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
# print(app_id,app_key,secret_key)
client = AipOcr(app_id, app_key, secret_key)

# 通用文字识别
# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content('test2.png')

# """ 调用通用文字识别, 图片参数为本地图片 """
# client.basicGeneral(image)

""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "false"
options["probability"] = "true"

""" 带参数调用通用文字识别, 图片参数为本地图片 """
result=client.basicGeneral(image,options)
print(result)

# url='https://login.sina.com.cn/cgi/pin.php?r=22096102&s=0&p=gz-05ed9d55e4ac216b91a163eb4f8476603875'
# """ 调用通用文字识别, 图片参数为远程url图片 """
# client.basicGeneralUrl(url)

# """ 如果有可选参数 """
# options = {}
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
#
# """ 带参数调用通用文字识别, 图片参数为远程url图片 """
# result=client.basicGeneralUrl(url)
# print(result)

""" 如果有可选参数 """
options = {}
options["detect_direction"] = "false"
options["probability"] = "true"

""" 带参数调用通用文字识别（高精度版） """
result=client.basicAccurate(image)
print(result)


""" 调用网络图片文字识别, 图片参数为本地图片 """
result=client.webImage(image)
print(result)