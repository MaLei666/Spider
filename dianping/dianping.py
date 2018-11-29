#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-11-29 12:05
# @file : dianping.py
# @software : PyCharm

import requests,pymysql
from bs4 import BeautifulSoup
from lxml import etree
def connect_mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zkyr1006',
        db='zhihu',
        charset='utf8'
    )
    cursor = conn.cursor()
    return conn,cursor

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Accept-Encoding':'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Upgrade-Insecure-Requests':'1'
}

start_url='http://www.dianping.com/beijing/food'
res=requests.get(start_url,headers=headers).text
soup=BeautifulSoup(res,'lxml')
print(soup)
# response=etree.HTML(res)
hot_url=soup.xpath('//div[@class="item news_list current"/a[@class="more"]/@href')
print(hot_url)
