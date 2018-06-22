# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # user_id=scrapy.Field()
    # user_img=scrapy.Field()
    question=scrapy.Field()
    que_url=scrapy.Field()
    name=scrapy.Field()
    # location=scrapy.Field()
    # business=scrapy.Field()
    # gender=scrapy.Field()
    # employment=scrapy.Field()
    # position=scrapy.Field()
    # education=scrapy.Field()
    content=scrapy.Field()
    num=scrapy.Field()

# class RelatinoItem(scrapy.Item):
#     user_id=scrapy.Field()
#     relation_type=scrapy.Field()
#     relation_id=scrapy.Field()



