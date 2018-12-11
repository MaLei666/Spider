#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm

from datetime import datetime as dt
from dianping import *
import re
from bs4 import  BeautifulSoup

def get_id():
    # 从数据库获取店铺id
    cursor,conn=connect_mysql()
    shopid_sql='SELECT shopId FROM food_rank;'
    cursor.execute(shopid_sql)
    shopid_list=list(cursor.fetchall())
    for each in shopid_list[:]:
        shopid_list.append(each[0])
        shopid_list.remove(each)
    shopid_list=set(shopid_list)
    cursor.close()
    conn.close()
    return shopid_list
    # print(shopid_list,len(shopid_list))



def get_shop_info():
    shopid_list = get_id()
    base_url = 'http://www.dianping.com/shop/'
    for shop_id in shopid_list:
        info_url=base_url+shop_id+'/review_all'
        try:
            res=request_set(info_url)
            good_count = res.xpath('//label[@class="filter-item filter-good"]/span/text()')[0][1:-1]
            middle_count = res.xpath('//label[@class="filter-item filter-middle"]/span/text()')[0][1:-1]
            bad_count = res.xpath('//label[@class="filter-item filter-bad"]/span/text()')[0][1:-1]
            re_num = res.xpath('//span[@class="active"]/em/text()')[0][1:-1]
            pages = res.xpath('//div[@class="reviews-pages"]/a[last()-1]/text()')[0]
            tags=res.xpath('//div[@class="reviews-tags"]/div[@class="content"]//span/a/text()')
            for each in tags[:]:
                re_each=clear_text(each)
                tags.append(re_each)
                tags.remove(each)
            print(good_count,middle_count,bad_count,re_num,pages,tags)

            get_rewiew_info(res)

            if pages>=2:
                for i in range(2,pages+1):
                    rewiew_url=info_url+'/p'+str(i)
                    res = request_set(rewiew_url)
                    get_rewiew_info(res)
        except:
            print('请求异常')

def get_rewiew_info(res):
    texts = []
    try:
        soup = BeautifulSoup(res.text(), 'lxml')
        reviews = soup.find_all(class_='review-words Hide')
        for each in reviews:
            review = each.get_text()[:-7]
            texts.append(review)
        texts = clear_text(texts)
        print(texts)


    except:
        # 后期添加tenserflow识别验证码
        # if text.xpath('//div[@_slider__sliderTitle___119tD]/p') or text.xpath('yodaModuleWrapper'):
        #     print('需要验证码')
        #     sleep(10)
        #     # 如果是滑动验证，模拟滑动
        # else:
        print('页面爬取错误')


from lxml import etree
# get_shop_info()
text=open('test.txt',encoding='utf-8')
text1=etree.HTML(text.read())
get_rewiew_info(text1)