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
        # 女装、男装、内衣
        # sub_navs1=page.xpath('//ul[@class="service-bd"]/li[position()<2]/a/text()').extract()
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
        # 连衣裙、毛衫/内搭、秋外套……
        sub_navs11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/text()').extract()
        del sub_navs11[-1]
        sub_urls11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/@href').extract()
        del sub_urls11[-1]
        # print(sub_navs11,'\n',sub_urls11)
        # for sub_url in sub_urls11:
        for i in range(0,len(sub_urls11)):
            page_urls=[]
            page_urls.append(sub_urls11[i]+'&sort=sale-desc')
            s=0
            sub_nav=sub_navs11[i]
            # for j in range(1,101):
            for j in range(0, 1):
                senddata = {
                    'sort':'sale-desc',
                    'bcoffset': '0',
                    's': s
                }
                page_url=sub_urls11[i]+'&'+ urlencode(senddata)
                page_urls.append(page_url)
                s+=60
            # print(page_urls)

            for page_url in page_urls:
                # self.goods_class = re.compile(u'[^\u4E00-\u9FA5]').sub(r'', page_url)
                # print(page_url,self.goods_class)
                yield SplashRequest(page_url,self.parse1,args={'wait':0.5},splash_headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})
                # yield scrapy.Request(page_url,callback=self.parse1,headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})


    def parse1(self, response):
        headers3 = {
            'Connection': 'keep-alive',
            'Host': 'item.taobao.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
        }
        page=Selector(response)
        # 每页取两个来测试
        goods_urls=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div[position()<2]/div[3]/div[2]/a/@href').extract()
        # goods_class=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div[1]/div[3]/div[2]/a/span[@class="H"]/text()').extract()
        goods_class=response.meta['sub_nav']
        # print(goods_urls)
        for goods_url in goods_urls:
            goods_url='http:'+goods_url
            yield scrapy.Request(goods_url,self.parse2,headers=headers3,dont_filter=True,meta={'goods_url':goods_url,'goods_class':goods_class})
            # yield SplashRequest(goods_url,self.parse2,splash_headers=headers2,dont_filter=True,args={'wait':1},meta={'goods_url':goods_url,'goods_class':goods_class})

    def parse2(self, response):
        item=TaobaoItem()
        page=Selector(response)
        # print(response.text)
        item['title']=page.xpath('//head/title/text()').extract()[0][:-4]
        item['goods_url']=response.meta['goods_url']
        item['goods_class']=response.meta['goods_class']
        item['price']=page.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()[0]
        item['comment']=page.xpath('//strong[@id="J_RateCounter"]/text()').extract()[0]
        # item['trade']=page.xpath('//div[@class="tb-sell-counter"]/a/strong/text()').extract()
        try:
            item['img_url']=page.xpath('//li[@data-index="0"]/div/a/img/@src').extract()[0]
        except:
            item['img_url']='无'

        try:
            item['seller']=page.xpath('//div[@class="tb-shop-name"]/dl/dd/strong/a/@title').extract()[0]
        except IndexError:
            item['seller']=page.xpath('//span[@class="shop-name-title"]/@title').extract()[0]
        except:
            item['seller']='未知'

        # print(item)
        yield item



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






