#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm

from datetime import datetime as dt
from dianping import *
import requests,random
from fake_useragent import UserAgent
ua = UserAgent()


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
    cookie_data = {'name': conf.get('cookies','name'),
                   'value':conf.get('cookies','value') }

    headers = {'User-Agent': ua.random,
               'Cookie': 'dper=value=3b07bb25d232ef657f838755d674ec07f9e0b5d54040c90c9880134a7b0df80ae03a9f0f9f758043e333d118da937eec73bcd014e6be0b1f6c744f3684831d081a6de9f7ca661a60f4ff913fdfe4208d346747bec5205da115c08c6d37041b1d',
               'Referer': 'http://www.dianping.com/shop/518986/review_all',
               'Connection':'keep-alive',
               'Host': 'www.dianping.com',
               }

    for shop_id in shopid_list:
        search_url = base_url + shop_id+'/review_all/p'+str(num)
        # search_url = base_url + shop_id
        print(search_url)
        try:
            import random
            sleep(random.random()*3+2)
            # browser.get(search_url,timeout=5,headers=headers)
            r=requests.get(url=search_url,timeout=5,headers=headers)
            # sleep(1)
            # # dper控制保持登录
            # browser.add_cookie(cookie_data)
            # browser.get(search_url)
            print(browser.page_source)

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