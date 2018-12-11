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
        reviews = text.xpath('//div[@class="reviews-items"]/ul//li/div/div[@class="review-words Hide"]/text()')
        reviews=clear_text(reviews)
        reviews=''.join(reviews)
        print(reviews)
    except:
        if text.xpath('//div[@_slider__sliderTitle___119tD]/p') or text.xpath('yodaModuleWrapper'):
            # 后期添加tenserflow识别验证码
            print('需要验证码')
            sleep(10)
            # 如果是滑动验证，模拟滑动

        else:
            print('页面爬取错误')


from lxml import etree
# get_shop_info()
text=open('test.txt',encoding='utf-8')
# text=etree.HTML(text.read())
texts=[]
soup=BeautifulSoup(text,'lxml')
soup=soup.find_all(class_='review-words Hide')
for each in soup:
    a=each.get_text()[:-7]
    texts.append(a)
a=clear_text(texts)

print(a)

# get_rewiew_info(text)