# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class CsdnScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章名
    title = scrapy.Field()
    # 文章链接
    url = scrapy.Field()
    # 文章简介
    text = scrapy.Field()
