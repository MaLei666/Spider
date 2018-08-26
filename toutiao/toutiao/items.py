# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 新闻标题
    title=scrapy.Field()
    # 新闻链接
    source_url=scrapy.Field()
    # 新闻简介
    abstract=scrapy.Field()
    # 新闻来源
    source=scrapy.Field()
    # 新闻标签
    tag=scrapy.Field()
    # 中文标签
    chinese_tag=scrapy.Field()
    # 新闻分类
    news_class=scrapy.Field()

