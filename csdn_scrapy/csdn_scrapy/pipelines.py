# -*- coding: utf-8 -*-
from csdn_scrapy import settings
from scrapy import Request
import requests,os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CsdnScrapyPipeline(object):
    def process_item(self, item, spider):
        dir_path='%s/%s'%(settings.ARTICLE_STORE,item['title'])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # for each in item['']


        return item
