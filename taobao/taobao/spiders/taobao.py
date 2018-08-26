# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from taobao.items import TaobaoItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import requests,re
from scrapy_splash import SplashRequest


# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    # 自己定义的内容，在运行工程的时候需要用到的标识；
    # 用于区别Spider。该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = 'tb'
    # 允许爬虫访问的域名，防止爬虫跑飞
    allowed_domains=['www.taobao.com']
    # start_urls:包含了Spider在启动时进行爬取的url列表。 第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls=['https://www.taobao.com']

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.taobao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    def start_requests(self):
        # yield SplashRequest(self.start_urls[0],self.sub_nav,splash_headers=self.headers,args={'wait':0.5})
        yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers)

    def sub_nav(self, response):
        # res=response.text
        page=Selector(response)
        sub_navs1=page.xpath('//ul[@class="service-bd"]/li[position()<3]/a/text()').extract()
        # print(sub_navs1)
        sub_urls1=page.xpath('//ul[@class="service-bd"]/li[position()<3]/a/@href').extract()
        # print(sub_urls1)
        for sub_url in sub_urls1:
            yield scrapy.Request(url=sub_url,callback=self.parse0,headers=self.headers,meta={'sub_navs1':sub_navs1})

    def parse0(self, response):
        page=Selector(response)
        sub_navs1=response.meta['sub_navs1']
        sub_navs11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/text()').extract()
        sub_urls11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/@href').extract()
        # print(sub_navs11,'\n',sub_urls11)
        for sub_url in sub_urls11:
            print(sub_url)
            yield SplashRequest(url=sub_url,callback=self.parse1,splash_headers=self.headers)

    def parse1(self, response):
        page=Selector(response)
        urls=[]
        s=0
        pages=page.xpath('[//div[@inner clearfix]/ul[@class="items"/div[1]/text()')[1:-1]
        print(pages)
        for i in range(1,int(pages)):
            url='https://s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009&bcoffset=12&s='+s
            s+=60
            urls.append(url)
        print(urls)


# //s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009
#
# //s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009&bcoffset=12&s=60
#
# //s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009&bcoffset=12&s=120
#
# //s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009&bcoffset=12&s=180
#
# //s.taobao.com/list?spm=a217f.8051907.249291-static.1.54af3308Uf46qT&q=%E8%BF%9E%E8%A1%A3%E8%A3%99&style=grid&seller_type=taobao&cps=yes&cat=51108009&bcoffset=12&s=240

