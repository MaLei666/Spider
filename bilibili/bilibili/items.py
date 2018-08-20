# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 视频名称
    title = scrapy.Field()
    # 视频类别
    class_v=scrapy.Field()
    # 视频链接
    url = scrapy.Field()
    # 视频简介
    text = scrapy.Field()
    # 观看人数
    people=scrapy.Field()
    # 弹幕数量
    danmu=scrapy.Field()
    # 所属分类
    class_name=scrapy.Field()
