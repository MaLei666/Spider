#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_cookies.py
# @software : PyCharm

from time import sleep
from dianping import *

browser=browser_set()

try:
    browser.get('http://account.dianping.com/login')
    # 跳转到登录的iframe，不然获取不到元素
    login_frame = browser.find_element_by_xpath('.//div[@id="J_login_container"]/div/iframe')
    browser.switch_to_frame(login_frame)
    sleep(4)
    browser.find_element_by_class_name('bottom-password-login').click()
    sleep(2)
    browser.find_element_by_id('tab-account').click()
    sleep(2)
    phone=browser.find_element_by_id('account-textbox')
    phone.send_keys('')
    pw=browser.find_element_by_id('password-textbox')
    pw.send_keys('')
    sleep(2)
    browser.find_element_by_id('login-button-account').click()
    try:
        captcha_test=browser.find_element_by_id('captcha-account-container')
        img=browser.find_element_by_class_name('captcha')
        print('需要验证码')

    except:
        cookie_items=browser.get_cookies()
        cookie_Data={}
        for cookie in cookie_items:
            cookie_Data[cookie['name']]=cookie['value']
        print(cookie_items)
        file=open('cookie.txt','w',encoding='utf-8')
        file.write(cookie_Data[0]['value'])
        file.close()
    sleep(5)

finally:
    pass
    # browser.close()





# a={'domain': '.dianping.com',
#    'expiry': 1544078890.305766,
#    'httpOnly': False,
#    'name': 'lgtoken',
#    'path': '/',
#    'secure': False,
#    'value': '032f58fcf-f61e-4252-b0f1-e177e5b63d3b'}