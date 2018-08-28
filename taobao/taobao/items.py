# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_url=scrapy.Field()
    title=scrapy.Field()
    price=scrapy.Field()
    comment =scrapy.Field()
    goods_class=scrapy.Field()
    img_url=scrapy.Field()
    seller=scrapy.Field()

