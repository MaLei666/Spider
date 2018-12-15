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
    phone.send_keys(conf.get('account','phone'))
    pw=browser.find_element_by_id('password-textbox')
    pw.send_keys(conf.get('account','pw'))
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
        # file=open('cookie.txt','w',encoding='utf-8')
        # file.write(cookie_items[0]['value'])
        # file.close()
    sleep(5)

finally:
    pass
    # browser.close()

cookies=['cy=2; cye=beijing; _lxsdk_cuid=167b1995849c8-037c7551760f5d-10346654-13c680-167b199584ac8; _lxsdk=167b1995849c8-037c7551760f5d-10346654-13c680-167b199584ac8; _hc.v=e969b46d-7c06-6ddf-6814-7e3f42cf9d09.1544872876; dper=3b07bb25d232ef657f838755d674ec077d670ea2f0af420d657c27bdcc3ee0ddb978d5b8cbe918b29f492f939e933caf187d52888b9998d5f5f7e582b55d121f41f0346e2292fb322ff6f8407714921228578da028494ee16c6177b6fc39a71b; ll=7fd06e815b796be3df069dec7836c3df; ua=18401570769; ctu=32a871c547f64c71bccbced43bc31805a46afbe091777a08193483f3403d66c0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=167b231a5e4-b7b-af0-4ec%7C%7C188']