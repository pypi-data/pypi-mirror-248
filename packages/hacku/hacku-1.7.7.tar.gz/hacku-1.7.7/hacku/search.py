# coding=utf-8

import time
from urllib.parse import quote

import requests
import shodan
from bs4 import BeautifulSoup
from loguru import logger

from hacku import UA


def get_url_from_google(query, proxy_url):
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    # 爬取网页html源码
    query = query.replace(' ', '+')
    url = 'https://google.com/search?q={q}&num=100'.format(q=quote(query, safe="+"))
    logger.info(url)
    response = requests.get(url, headers={"User-Agent": UA.get_random_user_agent()}, proxies=proxies)
    results = []
    if response.status_code == 200:
        # 使用BeautifulSoup解析html对象，并使用正则表达式查找目标内容
        html = BeautifulSoup(response.text, 'html.parser')
        for item in html.find_all('a'):
            s = item.get('href')
            if '/url?q=' not in s or '.google.' in s:
                continue
            u = s.split('/url?q=')[1].split('&sa=')[0]
            results.append(u)
    else:
        logger.error('Request Failed!')
    return results


def search_shodan(query, api_key) -> list:
    res = list()
    try:
        api = shodan.Shodan(api_key)
        result_number = api.count(query)
        total = result_number['total']
        logger.info("Search query: %s has %s result" % (query, total))

        cnt = 0
        check = 0
        _page = 1
        while True:
            try:
                tmp_limit = int(total) - cnt
                if tmp_limit < 100:
                    result = api.search(query, page=_page)
                    check = 0
                    for r in result['matches']:
                        res.append({
                            "ip": r['ip_str'],
                            "domain": r['hostnames'],
                            "port": r['port'],
                            "ssl": 'ssl' in r
                        })
                    _page += 1
                    break
                result = api.search(query, page=_page)
                for r in result['matches']:
                    res.append({
                        "ip": r['ip_str'],
                        "domain": r['hostnames'],
                        "port": r['port'],
                        "ssl": 'ssl' in r
                    })
                check = 0
                cnt += 100
                _page += 1
            except shodan.exception.APIError:
                check += 1
                if check > 10:
                    break
                time.sleep(10)
    except shodan.APIError as e:
        logger.error(e)
    return res
