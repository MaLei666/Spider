#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 15:45
# @file : test.py
# @software : PyCharm
#
#
from dianping import *
from bs4 import BeautifulSoup

def get_rewiew_info(text):
    try:
        reviews = text.xpath('//div[@class="reviews-items"]/ul//li/div/div'
                             '[@class="review-words Hide"]/text()')
        reviews=clear_text(reviews)
        reviews=''.join(reviews)
        print(reviews)
    except:
        if text.xpath('//div[@_slider__sliderTitle___119tD]/p') or \
                text.xpath('yodaModuleWrapper'):
            # 后期添加tenserflow识别验证码
            print('需要验证码')
            sleep(10)
            # 如果是滑动验证，模拟滑动

        else:
            print('页面爬取错误')


from lxml import etree
# text=open('test.txt',encoding='utf-8')
# # text=etree.HTML(text.read())
# texts=[]
# soup=BeautifulSoup(text,'lxml')
# soup=soup.find(text='验证中心')
# for each in soup:
#     a=each.get_text()[:-7]
#     texts.append(a)
# a=clear_text(texts)
cookie_items=['cy=2; cye=beijing; _lxsdk_cuid=167b1995849c8-037c7551760f5d-10346654-13c680-167b199584ac8; _lxsdk=167b1995849c8-037c7551760f5d-10346654-13c680-167b199584ac8; _hc.v=e969b46d-7c06-6ddf-6814-7e3f42cf9d09.1544872876; dper=3b07bb25d232ef657f838755d674ec077d670ea2f0af420d657c27bdcc3ee0ddb978d5b8cbe918b29f492f939e933caf187d52888b9998d5f5f7e582b55d121f41f0346e2292fb322ff6f8407714921228578da028494ee16c6177b6fc39a71b; ll=7fd06e815b796be3df069dec7836c3df; ua=18401570769; ctu=32a871c547f64c71bccbced43bc31805a46afbe091777a08193483f3403d66c0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=167b231a5e4-b7b-af0-4ec%7C%7C188']
cookie_Data = {}
for cookie in cookie_items:
    cookie_Data[cookie['name']] = cookie['value']
print(cookie_items)
file = open('cookie.txt', 'w', encoding='utf-8')
file.write(cookie_items[0]['value'])
file.close()

