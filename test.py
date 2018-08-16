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

# cate_id=[
#  24,25,47,27,33,32,51,152,153,168,169,170,28,31,30,59,29,54,130,20,154,156,17,171,172,65,173,121,136,19,124,122,39, 96,95,98,176,138, 21,76,75,161,162,163,174,22,26,126,127,157,158,164,159,71,137,131,182,183, 85,184,86]
from urllib.parse import urlencode

# ajax_urls = []
cate_id = [
 24, 25, 47, 27, 33, 32, 51, 152, 153, 168, 169, 170, 28, 31, 30, 59, 29, 54, 130, 20, 154, 156, 17, 171,
 172, 65, 173, 121, 136, 19, 124, 122, 39, 96, 95, 98, 176, 138, 21, 76, 75, 161, 162, 163, 174, 22, 26, 126,
 127, 157, 158, 164, 159, 71, 137, 131, 182, 183, 85, 184, 86]

headers = {
    'Connection': 'keep-alive',
    'Host': 's.search.bilibili.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
#
# # sub_nav_url=self.sub_nav_url
# for id in cate_id:
#  parse = {
#   'callback': 'jqueryCallback_bili_10',
#   'main_ver': 'v3',
#   'search_type': 'video',
#   'view_type': 'hot_rank',
#   'order': 'click',
#   'copy_right': '-1',
#   'cate_id': id,
#   'page': '1',
#   'pagesize': '20',
#   'jsonp': 'jsonp',
#   'time_from': '20180809',
#   'time_to': '20180816'
#  }
#  ajax_url = base_url + urlencode(parse)
base_url = 'https://s.search.bilibili.com/cate/search?'
parse = {
    'callback': 'jqueryCallback_bili_10',
    'main_ver': 'v3',
    'search_type': 'video',
    'view_type': 'hot_rank',
    'order': 'click',
    'copy_right': '-1',
    'cate_id': '26',
    'page': '1',
    'pagesize': '20',
    'jsonp': 'jsonp',
    'time_from': '20180809',
    'time_to': '20180816'
}

url = base_url + urlencode(parse)
print(url)
# url='https://s.search.bilibili.com/cate/search?callback=jqueryCallback_bili_23&main_ver=v3&search_type=video&view_type=hot_rank&order=click&copy_right=-1&cate_id='+'26'+'&page=10&pagesize=20&jsonp=jsonp&time_from=20180801&time_to=20180816'

response = requests.get(url,headers=headers,verify=False)
html=response.text

print(html)
# b=json.loads(html)
# c=b.decode(encoding='utf-8')
# print(c)
# a=response.json()
# a=demjson.encode(html)
# print(a)
# a1=json.loads(a)
# b=a1.encode(encoding='utf-8')
# print(b)
# resuit=json.loads(b)
# new=json.dumps(resuit,ensure_ascii=False)

# print(new)


# b=a.get('numPages')
# print(b)


