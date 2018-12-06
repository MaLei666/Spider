#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm


from datetime import datetime as dt
from dianping import *
import requests


# cookies={'lgtoken': '0d5bd5350-a194-4b50-8219-93ca76900779',
#          'dper': '3b07bb25d232ef657f838755d674ec0777aff6b188819326beed1a742d99713553b37593d78db18f441446937b45c5b55599fd87435c7d60f8946c98ea124168',
#          'll': '7fd06e815b796be3df069dec7836c3df',
#          'ua': '18401570769',
#          'ctu': '32a871c547f64c71bccbced43bc3180523918f0c4eb38f9391b358c90aa88b35',
#          'cy': '2',
#          'cye': 'beijing',
#          '_lxsdk_cuid': '1677e9bea08c8-0c6b569bbaafa68-4c312979-100200-1677e9bea095f',
#          '_lxsdk': '1677e9bea08c8-0c6b569bbaafa68-4c312979-100200-1677e9bea095f',
#          '_hc.v': 'd32a23ba-d92b-2376-076d-8ed45010328a.1544017407',
#          '_lxsdk_s': '1677e9bea0a-4fc-c01-ba2%7C%7C7'}

def get_id():
    # 从数据库获取店铺id
    cursor,conn=connect_mysql()
    search_url='http://www.dianping.com/shop/'
    shopid_sql='SELECT shopId FROM food_rank;'
    cursor.execute(shopid_sql)
    shopid_list=list(cursor.fetchall())
    for each in shopid_list[:]:
        shopid_list.append(each[0])
        shopid_list.remove(each)
    shopid_list=set(shopid_list)
    # print(shopid_list,len(shopid_list))
    for shop_id in shopid_list:
        search_url=search_url+shop_id
        data=requests.get(search_url,headers,proxies={"http": "http://{}".format(get_proxy())}).status_code
        print(data)
    cursor.close()
    conn.close()


browser=browser_set()
browser.get('http://www.dianping.com/')
# dper控制保持登录
cookie=open('cookie.txt').read()

print(cookie)

browser.add_cookie(
    {'name' : 'value',
     'value' : cookie})
browser.get('http://www.dianping.com/')