#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm

from datetime import datetime as dt
from dianping import *
import requests


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



def get_info():
    shopid_list=get_id()
    base_url = 'http://www.dianping.com/shop/'
    num=1
    browser = browser_set()
    # cookie_data = {'name': conf.get('cookies','name'),
    #                'value':conf.get('cookies','value') }

    for shop_id in shopid_list:
        # search_url = base_url + shop_id+'/review_all/p'+str(num)
        search_url = base_url + shop_id
        print(search_url)
        browser.get(search_url)

        # dper控制保持登录
        # browser.add_cookie(cookies)
        # browser.get(search_url)
        try:
            # splash_url = 'http://192.168.1.137:8050/render.html?url='+search_url
            # print(splash_url)
            # data = requests.get(splash_url, cookies=cookie_data,headers=headers)
            # print(data.text)
            # response = etree.HTML(data.text)
            # print(data)
            good_count = browser.find_element_by_xpath('//label[@class="filter-item filter-good"]/span/text()')
            middle_count=browser.find_element_by_xpath('//label[@class="filter-item filter-middle"]/span/text()')
            bad_count=browser.find_element_by_xpath('//label[@class="filter-item filter-bad"]/span/text()')
            pages=browser.find_element_by_xpath('//div[@class="reviews-pages"]/a[last()-1]/text()')
            print(good_count,middle_count,bad_count,pages)
            num+=1
        except:
            try:
                if browser.find_element_by_xpath('//div[@_slider__sliderTitle___119tD]/p') or browser.find_element_by_id('yodaModuleWrapper'):
                    print('需要验证码')
                sleep(10)
            except:
                print('页面爬取错误')
        finally:
            sleep(3)

get_info()