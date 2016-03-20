""":mod:`crawler.database` ---  MongoDB Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging

from pymongo import MongoClient

from .config import crawler_config


logger = logging.getLogger(__name__)


class MongoDB:

    def __init__(self, db: str):
        db_config = crawler_config.db_config
        client = MongoClient(host=db_config['url'],
                             serverSelectionTimeoutMS=3)
        self.collection = client[db]

    def query(self, document: str):
        return self.collection[document]

    def insert(self, document: str, *, data: dict):
        return self.collection[document] \
            .insert(data)

    def update(self, document: str, *, c, data: dict):
        return self.collection[document] \
            .update({'_id': c['_id']}, {'$set': data})
