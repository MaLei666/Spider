#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nl/bin python
# -*- coding: utf-8 -*-
# @Time           : 2018/11/28 21:10
# @Author         : MaLei
# @File           : dianping.py
# @Product        : PyCharm

import scrapy,numpy
from scrapy import Selector
from dianping.items import DianpingItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import requests,re
from scrapy_splash import SplashRequest
from urllib.parse import urlencode

class comicspider(scrapy.Spider):
    name = 'dp'
    allowed_domains=['dianping.com']
    start_urls=['http://www.dianping.com/shoplist/shopRank/pcChannelRankingV2?rankId=90dcc5b1cceea1afd8fd4f1a8cc5603571862f838d1255ea693b953b1d49c7c0']

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'Accept-Encoding':'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers)

    def sub_nav(self, response):
        page=Selector(response)
        # 分类最佳
        sub_navs1=page.xpath('//div[@class="box shopRankNav"]/p[1]//a[position()<3]/text()').extract()
        sub_navs2=page.xpath('//div[@class="box shopRankNav"]/p[2]//a/text()').extract()
        sub_navs=sub_navs1+sub_navs2
        print(sub_navs)
        sub_urls1=page.xpath('//div[@class="box shopRankNav"]/p[1]//a[position()<3]/@href').extract()
        sub_urls2=page.xpath('//div[@class="box shopRankNav"]/p[2]//a/@href').extract()
        sub_urls=sub_urls1+sub_urls2
        print(sub_urls)
        for sub_url in sub_urls:
            yield scrapy.Request(url=sub_url,callback=self.parse0,headers=self.headers,dont_filter=True)

    # def parse0(self, response):
    #     headers2 = {
    #         'Connection': 'keep-alive',
    #         'Host': 's.taobao.com',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    #     }
    #     page=Selector(response)
    #     # 连衣裙、毛衫/内搭、秋外套……
    #     sub_navs11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/text()').extract()
    #     del sub_navs11[-1]
    #     sub_urls11=page.xpath('//dl[@class="theme-bd-level2"]/dt/div/a/@href').extract()
    #     del sub_urls11[-1]
    #     for i in range(0,len(sub_urls11)):
    #         page_urls=[]
    #         page_urls.append(sub_urls11[i]+'&sort=sale-desc')
    #         s=0
    #         sub_nav=sub_navs11[i]
    #         for j in range(1,20):
    #         # for j in range(0, 1):
    #             senddata = {
    #                 'sort':'sale-desc',
    #                 'bcoffset': '0',
    #                 's': s
    #             }
    #             page_url=sub_urls11[i]+'&'+ urlencode(senddata)
    #             page_urls.append(page_url)
    #             s+=60
    #         # print(page_urls)
    #
    #         for page_url in page_urls:
    #             yield SplashRequest(page_url,self.parse1,args={'wait':0.5},splash_headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})
    #             # yield scrapy.Request(page_url,callback=self.parse1,headers=headers2,dont_filter=True,meta={'sub_nav':sub_nav})
    #
    # def parse1(self, response):
    #     headers3 = {
    #         'Connection': 'keep-alive',
    #         'Host': 'item.taobao.com',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    #     }
    #     page=Selector(response)
    #     goods_urls=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div/div[3]/div[2]/a/@href').extract()
    #     # goods_class=page.xpath('//div[@class="grid g-clearfix"]/div[@class="items"]/div[1]/div[3]/div[2]/a/span[@class="H"]/text()').extract()
    #     goods_class=response.meta['sub_nav']
    #     areas = page.xpath('//div[@class="row row-3 g-clearfix"]/div[@class="location"]/text()').extract()
    #     sell_counts=page.xpath('//div[@class="deal-cnt"]/text()').extract()
    #
    #     # print(goods_urls)
    #     for i in range(0,len(goods_urls)):
    #         area=areas[i]
    #         sell_count=sell_counts[i]
    #         goods_url='http:'+goods_urls[i]
    #         yield scrapy.Request(goods_url,self.parse2,headers=headers3,dont_filter=True,
    #                              meta={'goods_url':goods_url,
    #                                    'goods_class':goods_class,
    #                                    'area':area,
    #                                    'sell_count':sell_count})
    #
    # def parse2(self, response):
    #     item=TaobaoItem()
    #     page=Selector(response)
    #     # print(response.text)
    #     item['title']=page.xpath('//head/title/text()').extract()[0][:-4]
    #     item['goods_url']=response.meta['goods_url']
    #     item['goods_class']=response.meta['goods_class']
    #     item['price']=page.xpath('//strong[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract()[0]
    #     item['sell_count']=response.meta['sell_count'][:-3]
    #     item['area']=response.meta['area']
    #     # item['trade']=page.xpath('//div[@class="tb-sell-counter"]/a/strong/text()').extract()
    #     seller= page.xpath('//div[@class="tb-shop-name"]/dl/dd/strong/a/@title').extract()
    #     if len(seller)==1:
    #         item['seller']=seller[0]
    #     else:
    #         seller=page.xpath('//span[@class="shop-name-title"]/@title').extract()
    #         if len(seller)==1:
    #             item['seller'] = seller[0]
    #         else:
    #             seller = page.xpath('//span[@class="shop-name-title"]/@title').extract()
    #             if len(seller) == 1:
    #                 item['seller'] = seller[0]
    #             else:
    #                 item['seller'] = '未知'
    #
    #     yield item