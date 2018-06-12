# -*- coding: utf-8 -*-
import scrapy,re
from scrapy import Selector
from csdn_scrapy.items import CsdnScrapyItem

# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    # 自己定义的内容，在运行工程的时候需要用到的标识；
    # 用于区别Spider。该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = 'comic'

    def __init__(self):

        # 允许爬虫访问的域名，防止爬虫跑飞
        self.allowed_domains=['www.csdn.net']
        # start_urls:包含了Spider在启动时进行爬取的url列表。 第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
        self.start_urls=['https://www.csdn.net/nav/cloud']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.parse1)

    # 请求分析的回调函数，如果不定义start_requests(self)，获得的请求直接从这个函数分析
    # parse()是spider的一个方法。 被调用时，每个初始URL完成下载后生成的Response对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(responsedata)，提取数据(生成item) 以及生成需要进一步处理的URL的Request对象。

    # 解析response 获得文章url
    def parse1(self,response):
        items=[]
        hxs=Selector(response)
        # 文章名
        titles=hxs.xpath('//h2/a/text()').extract()
        # 文章链接
        urls=hxs.xpath('//h2/a/@href').extract()
        # text=hxs.xpath("//div[@class='summary oneline']/text()").extract()
        # 保存文章名和链接
        for i in range(len(titles)):
            item=CsdnScrapyItem()
            item['title']=titles[i].replace(' ','').replace('\n','')
            item['url']=urls[i]
            items.append(item)
            print(items[i])
        for item in items:
            yield scrapy.Request(url=item['url'],meta={'item':item},callback=self.parse2)

    def parse2(self, response):
        item=response.meta['item']
        item['url']=response.url

        print(item['url'])
        hxs=Selector(response)
        text=hxs.xpath('//article/text()').extract()
        item['text']=text[0]
        print(item['text'])
        yield item





