# coding=utf-8

from concurrent.futures import ProcessPoolExecutor
from urllib.parse import urlparse

import pymysql
import requests
from loguru import logger

from hacku import UA

session = requests.Session()


def test_proxy(proxy):
    try:
        if not proxy:
            return False
        response = session.get('https://ifconfig.me/ip', headers={'User-Agent': UA.get_random_user_agent(), 'Connection': 'close'},
                               proxies={'http': proxy, 'https': proxy}, timeout=3, verify=False)
        if response.status_code == 200:
            logger.debug(proxy)
            return True
    except:
        pass
    return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description='快速验证代理有效性')
    parser.add_argument('-i', type=str, help='代理节点文件路径')
    parser.add_argument('-o', type=str, help='可用代理节点存储文件路径')
    parser.add_argument('-m', type=str, help='代理节点数据库：mysql://username:password@host:port/db')
    parser.add_argument('-a', type=bool, default=True, help='是否全部测试，默认为True')
    args = parser.parse_args()
    db_uri = None

    proxies = list()
    if args.i:
        with open(args.i) as f:
            for l in f:
                if l.startswith('socks5://'):
                    proxies.append(l.strip())
    elif args.m:
        try:
            db_uri = urlparse(args.m)
            db_conn = pymysql.connect(host=db_uri.hostname, port=int(db_uri.port), user=db_uri.username, password=db_uri.password,
                                      database=db_uri.path.replace('/', ''), charset='utf8')
            with db_conn.cursor() as cursor:
                if args.a:
                    cursor.execute("SELECT concat('socks5://',username,':',password,'@',ip,':',port) as proxy FROM `proxy`")
                else:
                    cursor.execute("SELECT concat('socks5://',username,':',password,'@',ip,':',port) as proxy FROM `proxy` where valid=1")
                proxies = [r[0] for r in cursor.fetchall()]
            db_conn.close()
        except Exception as e:
            logger.error(e)
            exit(0)

    logger.info(f"待验证代理数量：{len(proxies)}")
    with ProcessPoolExecutor() as executor:
        results = executor.map(test_proxy, proxies)

    valid_proxies = list()
    db_data = list()
    for p, res in zip(proxies, results):
        if res:
            valid_proxies.append(p)
            tmp = urlparse(p)
            db_data.append((tmp.hostname, tmp.port))
    if args.m and db_data:
        db_conn = pymysql.connect(host=db_uri.hostname, port=int(db_uri.port), user=db_uri.username, password=db_uri.password,
                                  database=db_uri.path.replace('/', ''), charset='utf8')
        sql = "update proxy set valid=1 where ip=%s and port=%s"
        with db_conn.cursor() as cursor:
            cursor.execute("update proxy set valid=0")
            cursor.executemany(sql, db_data)
        db_conn.commit()
        db_conn.close()
    if args.o and valid_proxies:
        with open(args.o, 'a+') as f:
            f.writelines(valid_proxies)


if __name__ == '__main__':
    main()
