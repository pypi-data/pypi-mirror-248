# coding=utf-8

import requests
from loguru import logger


class OneAPI:
    def __init__(self, host, sys_token):
        self.host = host
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh,zh-CN;q=0.9',
            'referer': f'https://{host}/token',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
            'Authorization': sys_token,
            'X-Forwarded-For': '127.0.0.1'
        }

    def get_tokens(self):
        res = requests.get(f'https://{self.host}/api/token/?p=0', verify=False, headers=self.headers)
        logger.info(res.text)
        response = res.json()
        for d in response['data']:
            logger.info(f"名称：{d['name']}, key：{d['key']}, 过期时间：{d['expired_time']}, 余额：{d['remain_quota']}, 是否无限余额：{d['unlimited_quota']}")

    def get_token(self, name):
        response = requests.get(f'https://{self.host}/api/token/?p=0', verify=False, headers=self.headers).json()
        for d in response['data']:
            if d['name'] == name:
                return d['key']

    def add_token(self, name, money):
        json_data = {
            'name': name,
            'remain_quota': money * 500000,
            'expired_time': -1,
            'unlimited_quota': False,
        }

        response = requests.post(f'https://{self.host}/api/token/', verify=False, headers=self.headers, json=json_data).json()
        if response['success']:
            logger.info(f"添加成功: {name}")
            return self.get_token(name)
        else:
            logger.info("添加失败了，请联系管理员")

    def get_channel(self):
        response = requests.get(f'https://{self.host}/api/channel/?p=0', verify=False, headers=self.headers).json()
        logger.info(response)
        for d in response['data']:
            logger.info(f"名称：{d['name']}, key：{d['key']}, URL：{d['base_url']}, 余额：{d['remain_quota']}, 是否无限余额：{d['unlimited_quota']}")

    def add_channel(self, name, key, base_url, model):
        url = 'https://api.openai.com'
        if base_url:
            url = base_url
        json_data = {
            'name': name,
            'type': 1,
            'key': key,
            'base_url': url,
            'other': '',
            'model_mapping': '',
            'models': model,
            'group': 'default',
        }
        response = requests.post(f'https://{self.host}/api/channel/', verify=False, json=json_data, headers=self.headers).json()
        if response['success']:
            logger.info(f"添加成功: {key}")
