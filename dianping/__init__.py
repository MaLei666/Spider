

__all__=['connect_mysql','headers','get_proxy','requests','browser_set','conf','etree','sleep']

import pymysql,requests
from selenium import webdriver
from configparser import ConfigParser
from lxml import etree
from time import  sleep



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

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Accept-Encoding':'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Upgrade-Insecure-Requests':'1',
    'X-Requested-With':'XMLHttpRequest'
}


'''
代理启动步骤
cd /home/py_code/spider/
pipenv shell
cd proxy_pool/Run
python main.py
'''
def get_proxy():
    return requests.get("http://192.168.1.137:8001/get/").text


def browser_set():
    # 设置代理
    service_args = [
        '--proxy=%s' %get_proxy(), # 代理 IP：prot    （eg：192.168.0.28:808）
        '--ssl-protocol=any', #忽略ssl协议
        '--load - images = no', # 关闭图片加载（可选）
        '--disk-cache=yes', # 开启缓存（可选）
        '--ignore-ssl-errors=true' ]# 忽略https错误(可选)

    # 谷歌
    # options=webdriver.ChromeOptions()
    # # options.add_argument('--headless')
    # browser=webdriver.Chrome(options=options)

    # PhantomJS
    # user_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = user_Agent
    # browser=webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)

    # 火狐
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    browser=webdriver.Firefox(options=options,service_args=service_args)
    return browser

conf = ConfigParser()
conf.read('conf.ini')
