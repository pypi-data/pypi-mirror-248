# coding=utf-8
import copy
import random
import socket
import struct
import threading
import time
from socketserver import StreamRequestHandler, ThreadingTCPServer
from urllib.parse import urlparse

import pymysql
import requests
import select
import socks
from loguru import logger

from hacku import UA

SOCKS_VERSION = 5


class SocksProxy(StreamRequestHandler):
    username = ''
    password = ''

    def handle(self):
        address = bind_address = remote = None
        """
        一、客户端认证请求
            +----+----------+----------+
            |VER | NMETHODS | METHODS  |
            +----+----------+----------+
            | 1  |    1     |  1~255   |
            +----+----------+----------+
        """
        # 从客户端读取并解包两个字节的数据
        header = self.connection.recv(2)
        ver, nmethods = struct.unpack("!BB", header)
        # 设置socks5协议，METHODS字段的数目大于0
        assert ver == SOCKS_VERSION, 'SOCKS版本错误'
        # 接受支持的方法
        # 无需认证：0x00    用户名密码认证：0x02
        # assert NMETHODS > 0
        methods = self.is_available(nmethods)
        # 检查是否支持该方式，不支持则断开连接
        """ 
        二、服务端回应认证
            +----+--------+
            |VER | METHOD |
            +----+--------+
            | 1  |   1    |
            +----+--------+
        """
        # 发送协商响应数据包
        if self.username != '' and self.password != '':
            if 2 not in set(methods):
                logger.warning(f'[-] 客户端:  {self.client_address}  无账密信息，无法与客户端验证-已挂断连接')
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 2))
            if not self.verify_auth():
                return
        elif self.username == '' and self.password == '':
            if 0 not in set(methods):
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 0))
        """
        三、客户端连接请求(连接目的网络)
            +----+-----+-------+------+----------+----------+
            |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION, 'socks版本错误'
        if address_type == 1:  # IPv4
            # 转换IPV4地址字符串（xxx.xxx.xxx.xxx）成为32位打包的二进制格式（长度为4个字节的二进制字符串）
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain
            domain_length = ord(self.connection.recv(1))
            address = self.connection.recv(domain_length).decode()
        port = struct.unpack('!H', self.connection.recv(2))[0]
        """
        四、服务端回应连接
            +----+-----+-------+------+----------+----------+
            |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        # 响应，只支持CONNECT请求
        # 校验用户名和密码
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                p = socks.getdefaultproxy()
                logger.info(f'[+] 客户端:  {self.client_address}  已建立连接: {address, str(port)} 代理服务器: {":".join([p[1], str(p[2])])}')
            else:
                self.server.close_request(self.request)
            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type, addr, port)
        except Exception as err:
            logger.error(f'[-] 客户端:  {self.client_address} 连接: {address, str(port)}  发生错误: {err}')
            # 响应拒绝连接的错误
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 5, 0, address_type, 0, 0)
        self.connection.sendall(reply)  # 发送回复包
        # 建立连接成功，开始交换数据
        if reply[1] == 0 and cmd == 1:
            self.exchange_data(self.connection, remote)
        self.server.close_request(self.request)

    def is_available(self, n):
        """
        检查是否支持该验证方式
        """
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods

    def verify_auth(self):
        """
        校验用户名和密码
        """
        version = ord(self.connection.recv(1))
        assert version == 1
        username_len = ord(self.connection.recv(1))
        username = self.connection.recv(username_len).decode('utf-8')
        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')
        if username == self.username and password == self.password:
            # 验证成功, status = 0
            response = struct.pack("!BB", version, 0)
            self.connection.sendall(response)
            return True
        # 验证失败, status != 0
        logger.warning(f"[-] 客户端:  {self.client_address}  密码验证错误 已断开连接!")
        response = struct.pack("!BB", version, 0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False

    def exchange_data(self, client, remote):
        """
        交换数据
        """
        while True:
            # 等待数据
            try:
                rs, ws, es = select.select([client, remote], [], [])
                if client in rs:
                    data = client.recv(4096)
                    if remote.send(data) <= 0:
                        break
                if remote in rs:
                    data = remote.recv(4096)
                    if client.send(data) <= 0:
                        break
            except Exception as err:
                logger.error(f'客户端:  {self.client_address}  发生错误: {err}')
                pass


class ProxyPool:
    def __init__(self, nodes: list, username='', password='', rotate=5, detect=30 * 60):
        assert ((username and password) or (not username and not password))
        self.queue1 = nodes
        random.shuffle(self.queue1)
        self.queue2 = copy.deepcopy(self.queue1)
        self.detect_interval = detect
        self.rotate_interval = rotate
        SocksProxy.username = username
        SocksProxy.password = password

    def health_check(self):
        to_check = set(self.queue2)
        logger.info(f'对 {len(to_check)} 个节点进行健康检查')
        with requests.Session() as client:
            for n in to_check:
                try:
                    resp = client.get("http://ifconfig.me/ip", headers={'User-Agent': UA.get_random_user_agent()}, proxies={'http': n, 'https': n})
                    if resp.status_code == 200:
                        continue
                except:
                    pass
                self.queue1.remove(n)
                self.queue2.remove(n)

    def set_proxy(self):
        t1 = time.perf_counter()
        while True:
            t2 = time.perf_counter()
            if self.detect_interval != 0 and t2 - t1 >= self.detect_interval:
                self.health_check()

            if len(self.queue1) == 0:
                logger.info("重新刷新代理池")
                self.queue1 = copy.deepcopy(self.queue2)

            node = self.queue1.pop(0)
            if not node:
                continue

            try:
                n = urlparse(node)
                # 设置代理
                socks.set_default_proxy(socks.SOCKS5, n.hostname, n.port, rdns=True, username=n.username, password=n.password)
                socket.socket = socks.socksocket
                logger.warning(f'服务端当前代理服务器为：{n.hostname}:{n.port}, 剩余可用节点: {len(set(self.queue1))}')

                time.sleep(self.rotate_interval)

            except Exception as e:
                logger.error(f'代理服务器超时: {str(e)}')
                pass


def run(port):
    server = ThreadingTCPServer(('0.0.0.0', port), SocksProxy)
    server.serve_forever()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='socks5 代理池')
    parser.add_argument('-i', type=str, help='代理节点文件路径')
    parser.add_argument('-m', type=str, help='代理节点数据库：mysql://username:password@host:port/db')
    parser.add_argument('-p', type=int, default=18000, help='本地s5监听端口')
    parser.add_argument('-d', type=int, default=30, help='健康检查时间间隔 / 分钟')
    parser.add_argument('-r', type=int, default=5, help='代理轮换时间间隔 / 秒')
    args = parser.parse_args()

    all_nodes = set()
    if args.i:
        try:
            with open(args.i, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("socks5://"):
                        all_nodes.add(line.split('#')[0].strip())
        except Exception as e:
            logger.error(e)
            exit(0)
    elif args.m:
        try:
            db_uri = urlparse(args.m)
            conn = pymysql.connect(host=db_uri.hostname, port=int(db_uri.port), user=db_uri.username, password=db_uri.password,
                                   database=db_uri.path.replace('/', ''), charset='utf8')
            with conn.cursor() as cursor:
                cursor.execute("SELECT concat('socks5://',username,':',password,'@',ip,':',port) as proxy FROM `proxy` where valid=1")
                all_nodes = set([r[0] for r in cursor.fetchall()])
            conn.close()
        except Exception as e:
            logger.error(e)
            exit(0)
    else:
        logger.warning("必须指定代理数据源")
        exit(0)

    if not all_nodes:
        logger.warning('未读取到代理节点，请检查格式，务必以socks5://开头')
        exit(0)

    logger.info(f'成功读取{len(all_nodes)}个代理节点')

    pool = ProxyPool(list(all_nodes), rotate=args.r, detect=args.d * 60)
    threading.Thread(target=run, args=(args.p,)).start()

    time.sleep(0.5)
    pool.set_proxy()


if __name__ == '__main__':
    main()
