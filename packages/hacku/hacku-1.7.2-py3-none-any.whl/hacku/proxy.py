# coding=utf-8

from concurrent.futures import ProcessPoolExecutor

import requests
import urllib3
from loguru import logger

from hacku import UA

urllib3.disable_warnings()
session = requests.Session()


def test_proxy(proxy):
    try:
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
    parser.add_argument('-d', type=str, help='可用代理节点存储文件路径')
    args = parser.parse_args()

    proxies = list()
    with open(args.i) as f:
        for l in f:
            if l.startswith('socks5://'):
                proxies.append(l.strip())

    logger.info(f"读取代理数量：{len(proxies)}")
    with ProcessPoolExecutor() as executor:
        results = executor.map(test_proxy, proxies)

        # 处理结果
        with open(args.o, 'a+') as f:
            for p, res in zip(proxies, results):
                if res:
                    f.write(p + '\n')


if __name__ == '__main__':
    main()
