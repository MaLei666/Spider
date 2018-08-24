# -*- coding: utf-8 -*-
import urllib,sys,requests,scrapy,demjson,json,re
from bs4 import BeautifulSoup
# from urllib.parse import quote
from lxml import etree
from scrapy import Selector
from urllib.request import urlopen

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
import time,hashlib,execjs
#
# def get_as_cp():
#     # zz = {}
#     now = round(time.time())
#     print(now,type(now))
#     # 获取计算机时间
#     e = hex(now).upper()[2:]  # hex()转换一个整数对象为十六进制的字符串表示
#     print(e)
#     i = hashlib.md5(str(now).encode('utf-8')).hexdigest().upper()  # hashlib.md5().hexdigest()创建hash对象并返回16进制结果
#     if len(e) != 8:
#         zz = {'as': "479BB4B7254C150",
#               'cp': "7E0AC8874BB0985"}
#         return zz
#
#     n = i[:5]
#     a = i[-5:]
#     r = ""
#     s = ""
#     for i in range(5):
#         s = s + n[i] + e[i]
#     for j in range(5):
#         r = r + e[j + 3] + a[j]
#     zz = {
#         'as': "A1" + s + e[-3:],
#         'cp': e[0:3] + r + "E1"
#     }
#     print(zz)

# get_as_cp()

# js_file = open('E:/Spider/toutiao/toutiao/signature.js', 'r')
# signature_js = js_file.read()
# print(signature_js)
# signature = execjs.compile(signature_js)
# si = signature.call('a')
#
# url='https://www.toutiao.com/'
# res=requests.get(url=url,verify=False).text
# print(res)

js_file=open('E:/Spider/toutiao/toutiao/signature.js','r').read()
signature=execjs.compile(js_file)
si=signature.call('a')