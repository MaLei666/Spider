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
text=open('test.txt',encoding='utf-8')
# text=etree.HTML(text.read())
texts=[]
soup=BeautifulSoup(text,'lxml')
# soup=soup.find(text='很抱歉，您要访问的页面不存在')[0]
# print(soup)

# if soup.find(text='验证中心') or soup.find(text='很抱歉，您要访问的页面不存在'):
#     # print(soup)
#     print('需要验证\n')
#     if input() == 1:
#         print('验证成功')


# for each in soup:
#     a=each.get_text()[:-7]
#     texts.append(a)
# a=clear_text(texts)
# cookie_items={'name': 'dper', 'value': '725ac95a9bd4cb990b26440742aa1fa5caed95e3cf2738c93a2ae1c6b9cb744c84c74fbb7894bf4a6e3516ec1d1f9d6ee448b8e42d5ffb2dd3f48e4f8c569237', 'path': '/', 'domain': '.dianping.com', 'secure': False, 'httpOnly': True, 'expiry': 1547777639}
# conf.set('cookies','value',cookie_items['value'])
# with open('conf.ini','w') as wr:
#     conf.write(wr)

pages=soup.find(class_='reviews-pages').find_all('a')[-2].get_text()
print(pages)