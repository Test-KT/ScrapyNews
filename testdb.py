import pymongo
from pymongo import IndexModel,ASCENDING
client=pymongo.MongoClient("mongodb://root:root@127.0.0.1/")

db=client['demo']

col=db['news']

idx=IndexModel([("link_url", ASCENDING)], unique=True)
col.create_indexes([idx])
# col.insert_one({'name':'lsl'})
col.update_one({'link_url': 'www.baidu.com'},{'$set':{'name':'lsl'}},upsert=True)
col.update_one({'link_url': 'www.baidu.com'},{'$set':{'name':'lsl'}},upsert=True)
col.update_one({'link_url': 'www.baidu.com1'},{'$set':{'name':'lsl'}},upsert=True)
