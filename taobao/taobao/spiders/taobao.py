# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from taobao.items import TaobaoItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import requests,re
from scrapy_splash import SplashRequest
from urllib.parse import urlencode


# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    # 自己定义的内容，在运行工程的时候需要用到的标识；
    # 用于区别Spider。该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = 'tb'
    # 允许爬虫访问的域名，防止爬虫跑飞
    allowed_domains=['www.taobao.com']
    # start_urls:包含了Spider在启动时进行爬取的url列表。 第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls=['https://www.taobao.com']

    headers1 = {
        'Connection': 'keep-alive',
        'Host': 'www.taobao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    def start_requests(self):
        # yield SplashRequest(self.start_urls[0],self.sub_nav,splash_headers=self.headers,args={'wait':0.5})
        yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers1)

    def sub_nav(self, response):
        # res=response.text
        page=Selector(response)
        sub_navs1=page.xpath('//ul[@class="service-bd"]/li[position()<2]/a/text()').extract()
        # print(sub_navs1)
        sub_urls1=page.xpath('//ul[@class="service-bd"]/li[position()<2]/a/@href').extract()
        # print(sub_urls1)
        for sub_url in sub_urls1:
            yield scrapy.Request(url=sub_url,callback=self.parse0,headers=self.headers1,dont_filter=True)

    def parse0(self, response):
        headers2 = {
            'Connection': 'keep-alive',
            'Host': 's.taobao.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        page=Selector(response)
        sub_navs11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/text()').extract()
        del sub_navs11[-1]
        sub_urls11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/@href').extract()
        del sub_urls11[-1]
        # print(sub_navs11,'\n',sub_urls11)
        for sub_url in sub_urls11:
            page_urls=[]
            page_urls.append(sub_url)
            s=0
            # for i in range(1,101):
            for i in range(1, 2):

                senddata = {
                    'sort':'sale-desc',
                    'bcoffset': '12',
                    's': s
                }
                page_url=sub_url+'&'+ urlencode(senddata)
                page_urls.append(page_url)
                s+=60
            # print(page_urls)

            for page_url in page_urls:
                yield SplashRequest(page_url,self.parse1,args={'wait':0.5},splash_headers=headers2,dont_filter=True)
                # yield scrapy.Request(page_url,callback=self.parse1,headers=self.headers,dont_filter=True)


    def parse1(self, response):
        headers2 = {
            'Connection': 'keep-alive',
            'Host': 'item.taobao.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        page=Selector(response)
        goods_urls=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div[position()<3]/div[3]/div[2]/a/@href').extract()
        # print(goods_urls)
        for goods_url in goods_urls:
            goods_url='http:'+goods_url
            yield scrapy.Request(goods_url,self.parse2,headers=headers2,dont_filter=True)

    def parse2(self, response):
        item=TaobaoItem()
        page=Selector(response)
        item['title']=page.xpath('//h3[@class="tb-main-title"]/@data-title').extract()
        print(item)



    def cleanInput(self, input):
        input = re.sub('\n+', '', input)
        input = re.sub(' +', '', input)
        input = re.sub('\t+', '', input)
        input = re.sub('\xa0', '', input)
        # input = bytes(input, 'UTF-8')
        # input = input.decode('ascii', 'igone')
        # input = re.sub('\[[0-9]*\]', "", input)
        return input

            # print(sub_url)
            # url='https://s.taobao.com/list?q=%E6%AF%9B%E9%92%88%E7%BB%87%E8%A1%AB&cat=16&style=grid&seller_type=taobao&spm=a217f.1215286.1000187.1'
    #         yield SplashRequest(sub_url,self.parse1,args={'wait':0.5},splash_headers=self.headers,meta={'sub_url':sub_url},dont_filter=True)
    #
    # def parse1(self, response):
    #     page=Selector(response)
    #     sub_url11=response.meta['sub_url']
    #     print(sub_url11)

        # pages=page.xpath('//div[@class="inner clearfix"]/div[1]/text()').extract()
        # print(pages)






