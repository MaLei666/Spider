# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id=scrapy.Field()
    user_img=scrapy.Field()
    name=scrapy.Field()
    location=scrapy.Field()
    business=scrapy.Field()
    gender=scrapy.Field()
    employment=scrapy.Field()
    position=scrapy.Field()
    education=scrapy.Field()

class RelatinoItem(scrapy.Item):
    user_id


