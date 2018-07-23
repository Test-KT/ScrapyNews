# -*- coding: utf-8 -*-

import json
import time
import pymongo
from pymongo import IndexModel, ASCENDING
from SougouNews.items import SougounewsItem


class SougounewsPipeline(object):
    def process_item(self, item, spider):
        return item


class SougounewsWriteJsonPipeline(object):
    def __init__(self):
        self.file = open(time.strftime('%m-%d-%H')+".json", 'w')

    def process_item(self, item, spider):

        str = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(str)

        return item


class SougounewsMongoDbPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://root:root@127.0.0.1/")
        db = self.client['SougouNews']
        self.Table = db['HotNews']
        idx = IndexModel([('link', ASCENDING)], unique=True)
        self.Table.create_indexes([idx])

    def process_item(self, item, spider):
        try:
            dic=dict(item)
            link=item['link']
            self.Table.update_one({'link': link}, {'$set': dic}, upsert=True)
        except Exception as e:
            print("出现异常了")

        return item

    def close_spider(self,spider):
        self.client.close()
