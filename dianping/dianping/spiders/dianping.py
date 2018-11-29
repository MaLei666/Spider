#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nl/bin python
# -*- coding: utf-8 -*-
# @Time           : 2018/11/28 21:10
# @Author         : MaLei
# @File           : dianping.py
# @Product        : PyCharm

import scrapy
from scrapy import Selector
from dianping.items import DianpingItem
from scrapy.spiders import CrawlSpider, Rule
import requests,re
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
from lxml import etree

class comicspider(scrapy.Spider):
    name = 'dp'
    allowed_domains=['dianping.com']
    start_urls=['http://www.dianping.com/beijing/food']

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.dianping.com',
        'Accept-Encoding':'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'Upgrade-Insecure-Requests':'1'
    }

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers)

    def sub_nav(self, response):
        page=Selector(response)
        # base_url='http://www.dianping.com'
        # print(response.text)
        hot_url=page.xpath('//div[@class="item news_list current"]/a[@class="more"]/@href')[0].extract()
        sub_urls=[]
        sub_navs=[]
        sub_urls.append(hot_url)
        sub_navs.append('热门')
        res = etree.HTML(requests.get('http://www.dianping.com'+hot_url,headers=self.headers).text)
        # print(res.text)
        # 分类最佳
        sub_navs1=res.xpath('//div[@class="box shopRankNav"]/p[1]//a/text()')
        sub_navs2=res.xpath('//div[@class="box shopRankNav"]/p[2]//a/text()')
        sub_navs+=(sub_navs1+sub_navs2)
        print(sub_navs)
        sub_rankid1=res.xpath('//div[@class="box shopRankNav"]/p[1]//a/@href')
        sub_rankid2=res.xpath('//div[@class="box shopRankNav"]/p[2]//a/@href')
        sub_urls+=(sub_rankid1+sub_rankid2)
        # print(sub_urls)
        for sub_url in sub_urls:
            # sub_url=base_url+sub_url
            print(sub_url)
            # yield scrapy.Request(url=sub_url,callback=self.parse0,headers=self.headers,dont_filter=True)
            yield SplashRequest(url=sub_url, callback=self.parse0, args={'wait': 0.5}, splash_headers=self.headers, dont_filter=True)

    def parse0(self, response):
        page=Selector(response)
        print(response.text)
        ranks=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr/td[@class="td-rank"]/div/text()')
        shopNames=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-shopName"]/a/span/text()')
        mainRegions=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-mainRegionName"]/div/text()')
        taste=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-refinedScore1"]/div/text()')
        environment=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-refinedScore2"]/div/text()')
        service=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-refinedScore3"]/div/text()')
        avgPrice=page.xpath('//section[@class="ranklist-table"]/table/tbody//tr[position()>1]/td[@class="td-avgPrice"]/div/text()')
        print(ranks,shopNames,mainRegions,taste,environment,service,avgPrice)












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