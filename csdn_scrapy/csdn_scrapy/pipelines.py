# -*- coding: utf-8 -*-
# from csdn_scrapy import settings
import pymongo
from scrapy.conf import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CsdnScrapyPipeline(object):
    # spider参数用不到但是不能删除，删除会报错
    # def process_item(self, item,spider):
    #     if 'text' in item:
    #         # text=item['text']
    #         # dir_path='%s/%s'%(settings.ARTICLE_STORE,item['title'])
    #         # if not os.path.exists(dir_path):
    #         #     os.makedirs(dir_path)
    #         # if os.path.exists(file_path):
    #         # # for text in item['text']:
    #         # #     # print(text)
    #         # #     file_path='%s/%s'%(dir_path,item['title']+'.doc')
    #         # #     if os.path.exists(file_path):
    #         # #         continue
    #         # #     with open(file_path,'w',encoding='utf-8') as article_dl:
    #         # #         article_dl.write(text)
    #         # file_path = '%s/%s' % (dir_path, item['title'] + '.doc')
    #         #     pass
    #         file_path='%s\%s'%(settings.ARTICLE_STORE,item['title']+'.doc')
    #         # print(file_path)
    #         if os.path.exists(file_path):
    #             print('文件存在！')
    #         else:
    #             with open(file_path,'w',encoding='utf-8') as article_dl:
    #                 article_dl.write(item['text'])
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get("MONGO_URL"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE")
        )

    def open_spider(self,spider):
        # url方式加上用户名和密码没有连接上MongoDB

        # host = settings["MONGODB_HOST"]
        # port = settings["MONGODB_PORT"]
        # mongo_url=settings["MONGO_URL"]
        # mongo_db=settings["MONGODB_DATABASE"]
        # mongo_sheet=settings["MONGODB_SHEETNAME"]
        # 创建MONGODB数据库链接
        # client = pymongo.MongoClient(host=host, port=port)
        # client = pymongo.MongoClient(mongo_url)
        # # 指定数据库
        # db = client[mongo_db]
        # self.post = db[mongo_sheet]
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]

    def process_item(self, item, spider):
        # data=dict(item)
        # self.post.insert(data)
        self.db['csdn'].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()









