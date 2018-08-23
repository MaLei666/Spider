# -*- coding: utf-8 -*-
import scrapy,time,hashlib
from scrapy import Selector
from toutiao.items import ToutiaoItem
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import requests,re
from scrapy_splash import SplashRequest


# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    # 自己定义的内容，在运行工程的时候需要用到的标识；
    # 用于区别Spider。该名字必须是唯一的，不可以为不同的Spider设定相同的名字。
    name = 'tt'
    # 允许爬虫访问的域名，防止爬虫跑飞
    allowed_domains=['www.toutiao.com']
    # start_urls:包含了Spider在启动时进行爬取的url列表。 第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls=['https://www.toutiao.com']

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.toutiao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],callback=self.sub_nav,splash_headers=self.headers,args={'wait':0.5},)
        # yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers)

    def sub_nav(self, response):
        page = Selector(response)
        # print(response.text)
        # 所有子标签的``
        sub_nav_tips1=page.xpath('//div[@class="channel"]/ul/li/a/@href').extract()
        del sub_nav_tips1[:2],sub_nav_tips1[-1]
        sub_nav_tips2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/@href').extract()
        sub_nav_tips=sub_nav_tips1+sub_nav_tips2

        sub_names1=page.xpath('//div[@class="channel"]/ul/li/a/span/text()').extract()
        del sub_names1[:2], sub_names1[-1]
        sub_names2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/span/text()').extract()
        sub_names=sub_names1+sub_names2


        ajax_url_base = 'https://www.toutiao.com/api/pc/feed/?'

        # print(sub_nav_url)

        for sub_nav_tip in sub_nav_tips:
            sub_nav_tip = sub_nav_tips[4:-1]
            send_data = {
                'category' : sub_nav_tip,
                'utm_source':'toutiao',
                'widen':'1',
                'max_behot_time':'',
                'max_behot_time_tmp':'',
                'tadrequire':'true',
                'as':'A1A55B173E0B004',
                'cp':'5B7EAB708004FE1',
                '_signature':'Vxj1WAAADGfe-czCZbMMyVcY9U'
            }



        # for sub_nav_tip in sub_nav_tips:
        #     sub_nav_tip = sub_nav_tips[4:-1]
        #     print(sub_nav_tip)
            # yield SplashRequest(sub_url,callback=self.parse,splash_headers=self.headers,args={'wait':0.5},meta={'sub_nav_urls':sub_nav_urls})


    # def parse(self, response):
    #     sub_nav_urls=response.meta['sub_nav_urls']







    #     hot_list_urls=[]
    #     self.nav_names=[]
    #     self.time_tip='/2018-08-20,2018-08-20'
    #     page = Selector(response)
    #     # 所有子标签的url
    #     sub_nav_urls=page.xpath('//ul[@class="sub-nav"]//li/a/@href').extract()
    #     # print(sub_nav_urls)
    #     # 测试一个子标签
    #     # sub_nav_urls=['//www.bilibili.com/v/kichiku/guide/?spm_id_from=333.92.primary_menu.61']
    #     # 构建所有子标签URL，测试是否具有热度排行的标签，有就保存URL，没有就忽略
    #     for sub_nav_url in sub_nav_urls:
    #         self.sub_nav_url = 'https:' + sub_nav_url
    #         res=requests.get(url=self.sub_nav_url,headers=self.headers).text
    #         html=BeautifulSoup(res,'lxml')
    #         # tip = res.xpath('//div[@class="left"]/ul/a[2]/@href').extract()
    #         tip=html.find_all(href=re.compile('#/all/click/0/1/'))
    #         # print(tip)
    #         if len(tip) != 0:
    #             hot_list_url = self.sub_nav_url + '#/all/click/0/1'+self.time_tip
    #             hot_list_urls.append(hot_list_url)
    #             # print(hot_list_urls)
    #         else:
    #             sub_nav_urls.remove(sub_nav_url)
    #     # print(sub_nav_urls)
    #     print(self.nav_names)
    #     for i in range(0,len(hot_list_urls)):
    #         yield SplashRequest(hot_list_urls[i],self.parse0,args={'wait':0.5},splash_headers=self.headers,meta={'hot_list_url':hot_list_urls[i]})
    #     # print(hot_list_urls)
    #
    #
    # def parse0(self,response):
    #     # print(response.text)
    #     page = Selector(response)
    #     hot_list_url=response.meta['hot_list_url'][:-23]
    #     all_videos=[]
    #     print(hot_list_url)
    #     # video_pages=page.xpath('//ul[@class="pages"]/li[last()-1]//text()').extract()
    #     try:
    #         video_pages=int(page.xpath('//ul[@class="pages"]/li[last()-1]//text()').extract()[0])
    #         # print(video_pages)
    #         for i in range(1,video_pages+1):
    #             all_videos.append(hot_list_url+str(i)+self.time_tip)
    #             # print(hot_url+str(i)+self.time_tip)
    #         # print(all_videos)
    #     except:
    #         all_videos.append(hot_list_url+'1'+self.time_tip)
    #
    #     for all_video in all_videos:
    #         print(all_video)
    #         yield SplashRequest(all_video,self.parse1,args={'wait':0.5},splash_headers=self.headers)
    #
    # def parse1(self, response):
    #     item = ToutiaoItem()
    #     page=Selector(response)
    #     try:
    #         titles=page.xpath('//ul[@class="vd-list mod-2"]/li/div/div[2]/a/text()').extract()
    #         urls=page.xpath('//ul[@class="vd-list mod-2"]/li/div/div[2]/a/@href').extract()
    #         texts=page.xpath('//ul[@class="vd-list mod-2"]/li/div/div[2]/div[@class="v-desc"]/text()').extract()
    #         peoples=page.xpath('//ul[@class="vd-list mod-2"]/li/div/div[2]/div[@class="v-info"]/span[1]/span/text()').extract()
    #         danmus=page.xpath('//ul[@class="vd-list mod-2"]/li/div/div[2]/div[@class="v-info"]/span[2]/span/text()').extract()
    #         class_name = page.xpath('//li[@class="on"]/a/text()').extract()
    #         item['class_name'] = class_name[0]
    #         for i in range(0,len(titles)):
    #             item['title'] = self.cleanInput(titles[i])
    #             item['url'] = urls[i]
    #             item['text'] = self.cleanInput(texts[i])
    #             item['people'] = peoples[i]
    #             item['danmu'] = danmus[i]
    #             yield item
    #     except:
    #         pass
    #
    def cleanInput(self,input):
        input = re.sub('\n+', '', input)
        input = re.sub(' +', '', input)
        input = re.sub('\t+', '', input)
        input = re.sub('\xa0', '', input)
        # input = bytes(input, 'UTF-8')
        # input = input.decode('ascii', 'igone')
        # input = re.sub('\[[0-9]*\]', "", input)
        return input

    def get_as_cp():
        zz = {}
        now = round(time.time())
        print(now)
        # 获取计算机时间
        e = hex(int(now)).upper()[2:]  # hex()转换一个整数对象为十六进制的字符串表示
        print(e)
        i = hashlib.md5(str(int(now))).hexdigest().upper()  # hashlib.md5().hexdigest()创建hash对象并返回16进制结果
        if len(e) != 8:
            zz = {'as': "479BB4B7254C150",
                  'cp': "7E0AC8874BB0985"}
            return zz
        n = i[:5]
        a = i[-5:]
        r = ""
        s = ""
        for i in range(5):
            s = s + n[i] + e[i]
        for j in range(5):
            r = r + e[j + 3] + a[j]
        zz = {
            'as': "A1" + s + e[-3:],
            'cp': e[0:3] + r + "E1"
        }
        print(zz)


