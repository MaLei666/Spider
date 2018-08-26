# -*- coding: utf-8 -*-
import scrapy,time,hashlib
from scrapy import Selector
from toutiao.items import ToutiaoItem
from scrapy.spiders import CrawlSpider, Rule
import requests,re,json
from scrapy_splash import SplashRequest
from urllib.parse import urlencode
from selenium import webdriver

# 创建一个Spider，必须继承 scrapy.Spider 类
class comicspider(scrapy.Spider):
    name = 'tt'
    allowed_domains=['www.toutiao.com']
    start_urls=['https://www.toutiao.com']

    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.toutiao.com',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
    }

    # 进入浏览器设置
    options = webdriver.ChromeOptions()
    # 设置中文
    options.add_argument('lang=zh_CN.UTF-8')
    options.set_headless()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"')
    brower = webdriver.Chrome(chrome_options=options)
    ajax_url_base = 'https://www.toutiao.com/api/pc/feed/?'

    def start_requests(self):
        yield SplashRequest(url=self.start_urls[0],callback=self.sub_nav,splash_headers=self.headers,args={'wait':0.5},)
        # yield scrapy.Request(url=self.start_urls[0],callback=self.sub_nav,headers=self.headers,dont_filter=True)

    def sub_nav(self, response):
        page = Selector(response)

        # print(response.text)
        # 所有子标签的url
        sub_nav_tips1=page.xpath('//div[@class="channel"]/ul/li/a/@href').extract()
        del sub_nav_tips1[:2],sub_nav_tips1[-1],sub_nav_tips1[1]
        sub_nav_tips2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/@href').extract()
        sub_nav_tips=sub_nav_tips1+sub_nav_tips2
        # print(sub_nav_tips)
        #子标签的名字
        sub_names1=page.xpath('//div[@class="channel"]/ul/li/a/span/text()').extract()
        del sub_names1[:2], sub_names1[-1],sub_names1[1]
        sub_names2=page.xpath('//div[@class="channel-more-layer"]/ul/li/a/span/text()').extract()
        sub_names=sub_names1+sub_names2
        # print(sub_names)
        # 每个子标签遍历
        for i in range(0,len(sub_nav_tips)):
            items=[]
            # 请求子标签页面
            self.brower.get('https://www.toutiao.com' + sub_nav_tips[i])
            # 返回秒时间戳
            now = round(time.time())
            # 获取signature加密数据
            signature = self.brower.execute_script('return TAC.sign(' + str(now) + ')')
            # print(signature)
            # 获取cookie
            cookie = self.brower.get_cookies()
            cookie = [item['name'] + "=" + item['value'] for item in cookie]
            cookiestr = '; '.join(item for item in cookie)
            # print(cookiestr)

            header1 = {
                'Host': 'www.toutiao.com',
                'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"',
                # 'Referer': 'https://www.toutiao.com/ch/news_hot/',
                "Cookie": cookiestr
            }

            send_data = {
                'category': sub_nav_tips[i][4:-1],
                'utm_source': 'toutiao',
                'widen': '1',
                'max_behot_time': now,
                '_signature': signature
            }
            # 拼接ajax URL
            url = self.ajax_url_base + urlencode(send_data)
            # print(url)
            html = requests.get(url, headers=header1, verify=False)
            # 返回json数据，解析
            json_datas = json.loads(html.text)['data']
            # print(json_datas)
            for json_data in json_datas:
                item = ToutiaoItem()
                # print(type(json_data))
                item['title']=json_data['title']
                # 有的字段为空
                try:item['source_url']='https://www.toutiao.com/a'+json_data['source_url'][7:]
                except: item['source_url']=''
                try:item['abstract']=json_data['abstract']
                except: item['abstract']=''
                try:item['source']=json_data['source']
                except: item['source']=''
                try:item['tag']=json_data['tag']
                except:item['tag']=''
                try:item['chinese_tag']=json_data['chinese_tag']
                except: item['chinese_tag']='无标签类别'
                item['news_class']=sub_names[i]
                yield item
        self.brower.quit()