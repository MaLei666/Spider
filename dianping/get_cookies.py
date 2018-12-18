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
    sleep(3)

    try:
        cookie_items=browser.get_cookie(name='dper')
        conf.set('cookies', 'value', cookie_items['value'])
        with open('conf.ini', 'w') as wr:
            conf.write(wr)

    except:
        captcha_test=browser.find_element_by_id('captcha-account-container')
        img=browser.find_element_by_class_name('captcha')
        print('需要验证码')
        if input() == 1:
            print('验证成功')
    sleep(5)

finally:
    browser.close()

