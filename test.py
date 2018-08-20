# -*- coding: utf-8 -*-
import urllib,sys,requests,scrapy,demjson,json,re
from bs4 import BeautifulSoup
# from urllib.parse import quote
from lxml import etree
from scrapy import Selector

# string='https://www.bilibili.com/v/technology/fun/#/all/click/0/1/2018-08-01,2018-08-15'
# string=quote(string)
# print(string)

# # res=requests.get('https://data.bilibili.com/log/web?0000141534390076684https://www.bilibili.com/v/douga/mmd/',allow_redirects=False)
# res=requests.post('https://api.bilibili.com/x/web-interface/search/default')
# # res=scrapy.Request('https://www.bilibili.com/v/kichiku/mad/#/all/click/0/1/2018-08-01,2018-08-15',callback=None)
# html=res.text
# # html=Selector(res)
# # print(html)
# soup=BeautifulSoup(html,'lxml')
# print(soup)
# # html=res.url
# print(soup.find_all(class_='page-item last'))

# a=['https://www.bilibili.com/v/douga/mad/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/douga/mmd/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/douga/voice/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/douga/other/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/anime/serial/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/anime/finish/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/anime/information/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/anime/offical/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/guochuang/chinese/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/guochuang/original/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/guochuang/puppetry/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/guochuang/information/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/original/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/cover/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/vocaloid/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/perform/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/coordinate/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/oped/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/music/collection/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/dance/otaku/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/dance/three_d/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/dance/demo/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/stand_alone/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/esports/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/mobile/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/online/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/board/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/gmv/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/music/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/game/mugen/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/fun/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/wild/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/speech_course/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/military/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/digital/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/mechanical/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/technology/automobile/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/funny/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/daily/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/food/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/animal/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/handmake/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/painting/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/sports/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/life/other/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/kichiku/guide/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/kichiku/mad/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/kichiku/manual_vocaloid/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/kichiku/course/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/fashion/makeup/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/fashion/clothing/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/fashion/aerobics/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/fashion/information/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/ent/variety/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/ent/star/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/ent/korea/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/cinephile/cinecism/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/cinephile/montage/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/cinephile/shortfilm/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/cinephile/trailer_info/#/all/click/0/1/2018-08-01,2018-08-15', 'https://www.bilibili.com/v/cinephile/tokusatsu/#/all/click/0/1/2018-08-01,2018-08-15']
# for i in a:
#     print(i)
from scrapy_splash import SplashRequest
from scrapy  import Selector


headers = {
    'Connection': 'keep-alive',
    'Host': 'www.bilibili.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}

# url=' https://www.bilibili.com/v/guochuang/chinese/#/all/click/0/1/2018-08-14,2018-08-15 '
#
# # res=SplashRequest(url=url,callback=None,args={'wait':0.5},splash_headers=headers)
# # res=Selector(res)
# res=requests.get(url)
# res=Selector(res)
# # res=etree.parse(res,etree.HTMLParser())
# # res=etree.tostring(html).decode('utf-8')
# video_pages = res.xpath('//ul[@class="nav-menu"]/li[last()-1]//text()').extract()
# print(video_pages)


res=requests.get('https://www.bilibili.com/',headers=headers)
hot_list_urls=[]
nav_names=[]
time_tip='/2018-08-17,2018-08-17'
page = Selector(res)
# 所有子标签的url
sub_nav_urls=page.xpath('//ul[@class="sub-nav"]//li/a/@href').extract()
# print(sub_nav_urls)

# 构建所有子标签URL，测试是否具有热度排行的标签，有就保存URL，没有就忽略
for sub_nav_url in sub_nav_urls:
    sub_nav_url1 = 'https:' + sub_nav_url
    res=requests.get(url=sub_nav_url1,headers=headers).text
    html=BeautifulSoup(res,'lxml')
    # tip = res.xpath('//div[@class="left"]/ul/a[2]/@href').extract()
    tip=html.find_all(href=re.compile('#/all/click/0/1/'))
    # print(tip)
    if len(tip) != 0:
        # if tip != []
        hot_list_url = sub_nav_url1 + '#/all/click/0/1'+time_tip
        nav_name=html.find_all(href=re.compile(sub_nav_url))[0]
        nav_name=Selector(nav_name)
        nav_name=nav_name.xpath('//text()').extract()

        print(nav_name)
        hot_list_urls.append(hot_list_url)
        # print(hot_list_urls)
    else:
        sub_nav_urls.remove(sub_nav_url)


