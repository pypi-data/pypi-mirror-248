# coding=utf-8

from loguru import logger
from pymongo import MongoClient


class MongoHelper:
    def __init__(self, uri, db, collection=None):
        self.client = MongoClient(uri)
        self.db = self.client[db]
        if collection:
            self.handle = self.db[collection]

    def get_handle(self):
        return self.handle

    def check_connection(self) -> bool:
        try:
            self.client.server_info()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def find_all(self, query: dict, fields=None, **condition):
        body = dict(query, **condition)
        if fields:
            return self.handle.find(body, fields)
        else:
            return self.handle.find(body)

    def find_one(self, query: dict, **condition):
        body = dict(query, **condition)
        return self.handle.find_one(body)

    def insert_one(self, doc: dict, **condition):
        return self.handle.insert_one(doc, **condition)

    def insert_many(self, docs: list, **condition):
        self.handle.insert_many(docs, **condition)

    def replace_one(self, query: dict, doc: dict, upsert: bool, **condition):
        self.handle.replace_one(query, doc, upsert, **condition)

    def update_one(self, query: dict, doc: dict, upsert=False):
        self.handle.update_one(query, doc, upsert=upsert)

    def update_all(self, query: dict, doc: dict, upsert=False):
        self.handle.update_many(query, doc, upsert=upsert)

    def delete_one(self, query: dict):
        self.handle.delete_one(query)

    def delete_many(self, query: dict):
        self.handle.delete_many(query)
