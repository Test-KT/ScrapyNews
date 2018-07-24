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
    """
    写数据到json文件
    """
    def __init__(self):
        self.file = open(time.strftime('%m-%d-%H')+".json", 'w')

    def process_item(self, item, spider):

        str = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(str)

        return item


class SougounewsMongoDbPipeline(object):
    """
    写入到mongodb中
    """
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://root:root@127.0.0.1/")
        db = self.client['SougouNews']
        self.Table = db['HotNews']
        idx = IndexModel([('title', ASCENDING)], unique=True)
        self.Table.create_indexes([idx])

    def process_item(self, item, spider):
        try:
            dic=dict(item)
            title=item['title']
            self.Table.update_one({'title': title}, {'$set': dic}, upsert=True)
        except Exception as e:
            pass

        return item

    def close_spider(self,spider):
        self.client.close()
