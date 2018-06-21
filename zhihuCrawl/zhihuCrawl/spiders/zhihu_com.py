# -*- coding: utf-8 -*-
import scrapy,json,time,hmac,base64
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from requests_toolbelt import MultipartEncoder
from hashlib import sha1


class ZhihuComSpider(scrapy.Spider):
    name = 'zhihu.com'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    rules = (Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent
        # 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    client_id='c3cef7c66a1843f8b3a9e6a1e3160e20'
    grant_type= 'password'
    source='com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)

    # 处理签名
    def get_signnature(self,grant_type,client_id,source,timestamp):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        hm=hmac.new(b'd1b964811afb40118a12068ff74a12f4',None,sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())


    def start_requests(self):
        # 进入登录页面,回调函数start_login()
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.start_login)  # meta={'cookiejar':1}


    def start_login(self,response):
        # 判断是否需要验证码
        need_cap=json.loads(response.body)['show_captcha']
        print(need_cap)
        if need_cap:
            print('需要验证码')
            yield scrapy.Request(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.capture,method='PUT')

        else:
            print('不需要验证码')
            post_url='https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data={
                'client_id':self.client_id,
                'grant_type':self.grant_type,
                'timestamp':self.timestamp,
                'source':self.source,
                'signature':self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp),
                'username':'+8618401570769',
                'password':'conglingkaishi0',
                'captcha':'',
                # 改为'cn'是倒立汉字验证码
                'lang':'en',
                'ref_source':'other_',
                'utm_source':''}
            yield scrapy.FormRequest(url=post_url,formdata=post_data,headers=self.headers,callback=self.check_login)

    def capture(self,response):
        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('获取img_base64的值失败！')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('zhihu.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = input('请输入验证码：')
        post_data = {
            'input_text': captcha
        }
        yield scrapy.FormRequest(
            url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
            formdata=post_data,
            callback=self.captcha_login,
            headers=self.headers
        )

    def captcha_login(self, response):
        try:
            cap_result = json.loads(response.body)['success']
            print(cap_result)
        except ValueError:
            print('关于验证码的POST请求响应失败!')
        else:
            if cap_result:
                print('验证成功!')
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            'client_id': self.client_id,
            'grant_type': self.grant_type,
            'timestamp': self.timestamp,
            'source': self.source,
            'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp),
            'username': '+8618401570769',
            'password': 'conglingkaishi0',
            'captcha': '',
            'lang': 'en',
            'ref_source': 'other_',
            'utm_source': ''}
        headers = self.headers
        headers.update({
            'Origin': 'https://www.zhihu.com',
            'Pragma': 'no - cache',
            'Cache-Control': 'no - cache'
        })
        yield scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=headers,
            callback=self.check_login
        )

    def check_login(self,response):
        # if len(json.loads(response.text)['refresh_token']) != 0:
        text_json=json.loads(response.text)
        # print(text_json)
        yield scrapy.Request('https://www.zhihu.com/people/wu-di-zui-jun-mei/activities', headers=self.headers,callback=self.user_info)

    def user_info(self,response):
        # text=response.text
        # print(text)
        name=response.xpath("//span[@class='ProfileHeader-name']").extract()
        print(name)
        location = response.xpath("//span[@class='ProfileHeader-name']").extract()
        business = response.xpath("//span[@class='ProfileHeader-name']").extract()
        gender = response.xpath("//span[@class='ProfileHeader-name']").extract()
        employment = response.xpath("//span[@class='ProfileHeader-name']").extract()
        position = response.xpath("//span[@class='ProfileHeader-name']").extract()
        education = response.xpath("//span[@class='ProfileHeader-name']").extract()



