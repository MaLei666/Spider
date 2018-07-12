# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
import redis


class ZhihucrawlPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        sheetname = settings["MONGODB_SHEETNAME"]

        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        db = client[dbname]
        # 存放数据的数据库表名
        self.post = db[sheetname]

        # host = settings["REDIS_HOST"]
        # port = settings["REDIS_PORT"]

        # 创建redis数据库链接
        # client = redis.Redis(host=host, port=port)

        # 连接池管理redis连接
        # pool=redis.ConnectionPool(host=host,port=port)
        # r=redis.Redis(connection_pool=pool)



    def process_item(self, item, spider):
        data=dict(item)
        self.post.insert(data)
        return item


# from pymongo import MongoClient
#
# client=MongoClient("mongodb://127.0.0.1:27017,127.0.0.1:27021,127.0.0.1:27022",replicaset='repset')
# print( client.python.find_one())