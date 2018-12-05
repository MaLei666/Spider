#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-11-29 12:05
# @file : dianping.py
# @software : PyCharm

import requests,pymysql,re
from bs4 import BeautifulSoup
from datetime import datetime as dt
from lxml import etree
def connect_mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zkyr1006',
        db='dianping',
        charset='utf8'
    )
    cursor = conn.cursor()
    return cursor,conn

def get_proxy():
    return requests.get("http://192.168.1.137:8001/get/").text

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Accept-Encoding':'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Upgrade-Insecure-Requests':'1',
    'X-Requested-With':'XMLHttpRequest'
}
# base_url='http://www.dianping.com'
# start_url='http://www.dianping.com/beijing/food'
# res=requests.get(start_url,headers=headers).text
# response=etree.HTML(res)
# hot_url=response.xpath('//div[@class="item news_list current"]/a[@class="more"]/@href')
# # print(hot_url)
# classifi_res=requests.get((base_url+hot_url[0]),headers).text
# response=etree.HTML(classifi_res)
#
# classifi1=hot_url+response.xpath('//div[@class="box shopRankNav"]/p[1]//a/@href')
# class_name1=['热门']+response.xpath('//div[@class="box shopRankNav"]/p[1]//a/text()')
#
# classifi2=response.xpath('//div[@class="box shopRankNav"]/p[2]//a/@href')
# class_name2=response.xpath('//div[@class="box shopRankNav"]/p[2]//a/text()')
#
# class_name=class_name1+class_name2
# classifi=classifi1+classifi2
# ajax_base_url='http://www.dianping.com/mylist/ajax/shoprank?rankId='
#
# for each in classifi[:]:
#     classifi.append(ajax_base_url+each.split('=')[1])
#     classifi.remove(each)
# # print(classifi,len(classifi))
# cursor,conn=connect_mysql()
# sql = 'CREATE TABLE IF NOT EXISTS food_rank(' \
#       'id INT UNSIGNED AUTO_INCREMENT,' \
#       'class VARCHAR(100) NOT NULL,' \
#       'classifi VARCHAR(100) NULL,' \
#       'class_id INT(100) NULL,' \
#       'rank INT(100) NULL,' \
#       'shopId VARCHAR(100) NOT NULL,' \
#       'shopName VARCHAR(100) NOT NULL,' \
#       'mainRegionName VARCHAR(100) NULL,' \
#       'taste FLOAT(10) NULL,' \
#       'environment FLOAT(10) NULL,' \
#       'service FLOAT(10) NULL,' \
#       'avgPrice INT(255) NULL,' \
#       'city_id INT(100) NULL,' \
#       'address VARCHAR(100) NULL,' \
#       'update_time DATE NULL,' \
#       'PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
# cursor.execute(sql)
# conn.commit()
# update_time=dt.now().date()
# for i in range(0,len(classifi)):
#     print(classifi[i],class_name[i])
#     num=1
#     data=requests.get(url=classifi[i],headers=headers).json()
#     shopdata=data['shopBeans']
#     cityid=data['cityId']
#     try:
#         for each in shopdata:
#             mainCategoryName=each['mainCategoryName']
#             shopName=each['shopName']
#             branchName=each['branchName']
#             if len(branchName)!=0:
#                 shopName=shopName+'('+branchName+')'
#             shopId=each['shopId']
#             mainRegionName=each['mainRegionName']
#             taste=each['refinedScore1']
#             environment=each['refinedScore2']
#             service=each['refinedScore3']
#             avgPrice=each['avgPrice']
#             address=each['address']
#             sql='INSERT INTO food_rank(class,class_id,classifi,rank,shopId,shopName,mainRegionName,taste,environment,service,avgPrice,city_id,address,update_time) ' \
#                 'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
#             cursor.execute(sql,(class_name[i],
#                                 i,
#                                 mainCategoryName,
#                                 num,
#                                 shopId,
#                                 shopName,
#                                 mainRegionName,
#                                 taste,
#                                 environment,
#                                 service,
#                                 avgPrice,
#                                 cityid,
#                                 address,
#                                 update_time))
#             conn.commit()
#             num+=1
#     except:
#         pass
#
# # 去重
# a='delete from food_rank where id in (select id from (select id from food_rank where id not in (select min(id) from food_rank group by class,shopName,rank)) as temple)'
# cursor.execute(a)
# conn.commit()


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
# print(proxie)
# cursor,conn=connect_mysql()
# search_url='http://www.dianping.com/shop/'
# shopid_sql='SELECT shopId FROM food_rank;'
# cursor.execute(shopid_sql)
# shopid_list=list(cursor.fetchall())
# for each in shopid_list[:]:
#     shopid_list.append(each[0])
#     shopid_list.remove(each)
# shopid_list=set(shopid_list)
# # print(shopid_list,len(shopid_list))
# for shop_id in shopid_list:
#     search_url=search_url+shop_id
#     data=requests.get(search_url,headers,proxies={"http": "http://{}".format(get_proxy())}).status_code
#     print(data)
# binary = FirefoxBinary('/etc/apport/blacklist.d/firefox')
# 设置代理
service_args = [
    # '--proxy=%s' %get_proxy(), # 代理 IP：prot    （eg：192.168.0.28:808）
    '--ssl-protocol=any', #忽略ssl协议
    '--load - images = no', # 关闭图片加载（可选）
    '--disk-cache=yes', # 开启缓存（可选）
    '--ignore-ssl-errors=true' ]# 忽略https错误(可选)

# user_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = user_Agent
# browser=webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)

options = webdriver.FirefoxOptions()
# options.add_argument('--headless')
browser=webdriver.Firefox(options=options)
# try:
#     browser.get('http://account.dianping.com/login')
#     # 跳转到登录的iframe，不然获取不到元素
#     login_frame = browser.find_element_by_xpath('.//div[@id="J_login_container"]/div/iframe')
#     browser.switch_to_frame(login_frame)
#     sleep(4)
#     browser.find_element_by_class_name('bottom-password-login').click()
#     sleep(2)
#     # browser.switch_to_frame(login_frame)
#     browser.find_element_by_id('tab-account').click()
#     sleep(2)
#     phone=browser.find_element_by_id('account-textbox')
#     phone.send_keys('18401570769')
#     pw=browser.find_element_by_id('password-textbox')
#     pw.send_keys('conglingkaishi0')
#     browser.find_element_by_id('login-button-account').click()
#     sleep(5)
#     try:
#         captcha_test=browser.find_element_by_id('captcha-account-container')
#         img=browser.find_element_by_class_name('captcha')
#         print('需要验证码')
#
#     except:
#         pass
#     cookie_items=browser.get_cookies()
#     post={}
#     for cookie in cookie_items:
#         post[cookie['name']]=cookie['value']
#     print(post)
#
# finally:
#     # browser.close()
#     pass
#     browser.close()


# cursor.close()
# conn.close()
cookies={'lgtoken': '0d5bd5350-a194-4b50-8219-93ca76900779',
         'dper': '3b07bb25d232ef657f838755d674ec0777aff6b188819326beed1a742d99713553b37593d78db18f441446937b45c5b55599fd87435c7d60f8946c98ea124168',
         'll': '7fd06e815b796be3df069dec7836c3df',
         'ua': '18401570769',
         'ctu': '32a871c547f64c71bccbced43bc3180523918f0c4eb38f9391b358c90aa88b35',
         'cy': '2',
         'cye': 'beijing',
         '_lxsdk_cuid': '1677e9bea08c8-0c6b569bbaafa68-4c312979-100200-1677e9bea095f',
         '_lxsdk': '1677e9bea08c8-0c6b569bbaafa68-4c312979-100200-1677e9bea095f',
         '_hc.v': 'd32a23ba-d92b-2376-076d-8ed45010328a.1544017407',
         '_lxsdk_s': '1677e9bea0a-4fc-c01-ba2%7C%7C7'}
browser.get('http://www.dianping.com/')
# dper控制保持登录
browser.add_cookie(
    {'name' : 'dper',
     'value' : '3b07bb25d232ef657f838755d674ec0777aff6b188819326beed1a742d99713553b37593d78db18f441446937b45c5b55599fd87435c7d60f8946c98ea124168'})


browser.get('http://www.dianping.com/')


