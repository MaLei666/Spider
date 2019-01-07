#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2019-01-07 17:00
# @file : baidu_API.py
# @software : PyCharm

from configparser import ConfigParser
conf = ConfigParser()

conf.read('conf.ini')
from aip import AipOcr

""" 你的 APPID AK SK """
app_id = conf.get('baidu','APP_ID')
app_key = conf.get('baidu','API_KEY')
secret_key = conf.get('baidu','SECRET_KEY')
print(app_id,app_key,secret_key)
client = AipOcr(app_id, app_key, secret_key)