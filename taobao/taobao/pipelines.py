# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class TaobaoPipeline(object):
    def __init__(self,redis_url):
        self.redis_url=redis_url

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URL")
        )

    def open_spider(self, spider):
        conn=pymysql.connect(host='192.168.1.137',
                             port=3306,
                             user='root',
                             password='zkyr1006',
                             database='tb',
                             charset='utf8')
        self.cursor=conn.cursor()



    def process_item(self, item, spider):
        sql='INSERT INTO students(id, name, age) values(%s, %s, %s)INSERT INTO students(id, name, age) values(%s, %s, %s)'
        self.cursor
        # if sheet.find_one({'goods_url':item['goods_url']}):
        #     print('数据已存在')
        # else:
        #     sheet.insert(dict(item))

        return item

