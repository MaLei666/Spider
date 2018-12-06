#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 15:45
# @file : test.py
# @software : PyCharm
#
# a={
#     'domain': '.dianping.com',
#      'expiry': 1544083227.04485,
#      'httpOnly': False,
#      'name': 'lgtoken',
#      'path': '/',
#      'secure': False,
#      'value': '07ddfc0a0-0742-4385-b243-28db6cfb98c2'
# }
#
# print(a['value'])
# # browser.get('http://www.dianping.com/')
# # # dper控制保持登录
# # browser.add_cookie(
# #     {'name' : 'value',
# #      'value' : '037e1bb24-4827-42da-8834-9f939126841c'})
# #
# #
# # browser.get('http://www.dianping.com/')
cookie=open('cookie.txt').read()
print(    {'name' : 'value',
     'value' : cookie})
print(cookie)