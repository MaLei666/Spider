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
        if 'text' in item:
            # text=item['text']
            # dir_path='%s/%s'%(settings.ARTICLE_STORE,item['title'])
            # if not os.path.exists(dir_path):
            #     os.makedirs(dir_path)
            # if os.path.exists(file_path):
            # # for text in item['text']:
            # #     # print(text)
            # #     file_path='%s/%s'%(dir_path,item['title']+'.doc')
            # #     if os.path.exists(file_path):
            # #         continue
            # #     with open(file_path,'w',encoding='utf-8') as article_dl:
            # #         article_dl.write(text)
            # file_path = '%s/%s' % (dir_path, item['title'] + '.doc')
            #     pass
            file_path='%s/%s'%(settings.ARTICLE_STORE,item['title']+ '.doc')
            if os.path.exists(file_path):
                pass
            with open(file_path,'w') as article_dl:
                article_dl.write(item['text'])
        return item
