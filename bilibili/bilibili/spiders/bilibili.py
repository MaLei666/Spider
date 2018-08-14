# -*- coding: utf-8 -*-
import scrapy,re
from scrapy import Selector
# from bilibili.items import BilibiliItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    # 自己定义的内容，在运行工程的时候需要用到的标识；
    # 用于区别Spider。该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = 'blbl'
    # 允许爬虫访问的域名，防止爬虫跑飞
    allowed_domains=['www.bilibili.com']
    # start_urls:包含了Spider在启动时进行爬取的url列表。 第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls=['https://www.bilibili.com/']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse0)

    # 请求分析的回调函数，如果不定义start_requests(self)，获得的请求直接从这个函数分析
    # parse()是spider的一个方法。 被调用时，每个初始URL完成下载后生成的Response对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(responsedata)，提取数据(生成item) 以及生成需要进一步处理的URL的Request对象。

    def parse0(self, response):
        page = Selector(response)
        urls=page.xpath('//ul[@class="nav-menu"]//li/a/@href').extract()
        print(urls)
