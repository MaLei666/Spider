# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests,pymysql
from pyquery import PyQuery as pq
from selenium import webdriver
from time import sleep

browser = webdriver.Firefox()
browser.get(url='https://m.weibo.cn/')
cookies={}
s = requests.session()
with open('E:\Spider\Ajax_微博\cookie.txt')as file:
    raw_cookies=file.read()
    for line in raw_cookies.split(';'):
        key,value=line.split('=',1)
        cookies[key]=value
        # print(cookies)
    for each in cookies.items():
        print(type(each))
        each=eval(each.__str__())
        browser.add_cookie({'name':each.key(),'value':each[key]})

# browser.add_cookie({'name':'M_WEIBOCN_PARAMS','value':'featurecode%3D20000320%26oid%3D4245425282732969%26luicode%3D20000061%26lfid%3D4245425282732969%26uicode%3D20000174%26fid%3Dhotword'})
browser.refresh()
# print(browser.page_source)
# if browser.find_element_by_class_name()



# wb_name = browser.find_element_by_class_name("W_input")
# wb_name.send_keys(input('输入博主ID：'))
# sleep(10)
# search = browser.find_element_by_class_name('W_ficon ficon_search S_ficon')
# search.click()
# sleep(5)
# bz_num = browser.find_element_by_class_name('name_txt')
# bz_num.click()
# sleep(5)
# # 开启了一个新页面，需要跳转到新页面
# handles = browser.window_handles
# browser.switch_to_window(handles[1])