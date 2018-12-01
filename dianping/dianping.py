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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# binary = FirefoxBinary('/etc/apport/blacklist.d/firefox')
browser=webdriver.Firefox()
try:
    browser.get('http://account.dianping.com/login')
    login=browser.find_element_by_class_name('bottom-password-login')
    login.click()
    change_frame=browser.find_element_by_class_name('tab tab-account ')
    change_frame.click()
    phone=browser.find_element_by_id('account-textbox')
    phone.send_keys('18401570769')
    pw=browser.find_element_by_id('password-textbox')
    phone.send_keys('ML255734...')
    login_button=browser.find_element_by_id('login-button-account')
    login_button.click()
    a=browser.get_cookies()
    print(a)
finally:
    browser.close()



# cursor.close()
# conn.close()





