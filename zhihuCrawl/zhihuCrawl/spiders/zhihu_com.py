# -*- coding: utf-8 -*-
import scrapy,json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from requests_toolbelt import MultipartEncoder


class ZhihuComSpider(scrapy.Spider):
    name = 'zhihu.com'
    allowed_domains = ['zhihu.com']
    # start_urls = ['http://zhihu.com/']

    rules = (Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)

    def start_requests(self):
        # 进入登录页面,回调函数start_login()
        return [scrapy.Request('https://www.zhihu.com/signin',callback=self.start_login,meta={'cookiejar':1})]


    def start_login(self,response):
        # 开始登录
        # self.xsrf=scrapy.Selector(response).xpath("//input[@class='Input']/@value").extract_first()
        return [scrapy.FormRequest('https://www.zhihu.com/signin',method='POST',meta={'cookiejar':response.meta['cookiejar']},
                formdata={
            'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type':'password',
            'timestamp':'1529030791765',
            'source':'com.zhihu.web',
            'signature':'455bde303384a25d3492273c20f05f5cfc9128d1',
            'username':'+8618401570769',
            'password':'conglingkaishi0',
            'lang':'cn',
            'ref_source':'other_'},
         callback=self.after_login
         )]

    def after_login(self,response):
        # if len(json.loads(response.text)['refresh_token']) != 0:
            print('登录成功')


