# -*- coding: utf-8 -*-
import requests,random,re,json,time,urllib,os
from urllib import request
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import etree
import subprocess as sp
from selenium import webdriver
from pyquery import pyquery as pq
# from pyExcelerator import *
from urllib.parse import quote
from bs4 import BeautifulSoup

webdriver.DesiredCapabilities.FIREFOX[
        'firefox.page.settings.userAgent'] = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
profile = webdriver.FirefoxProfile()
# profile.set_preference('network.proxy.type', 1)  # 默认值0，就是直接连接；1就是手工配置代理。
# profile.set_preference('network.proxy.http', ip)
# profile.set_preference('network.proxy.http_port', port)
# profile.set_preference('network.proxy.ssl', ip)
# profile.set_preference('network.proxy.ssl_port', port)

# profile.set_preference('network.proxy.http', '112.116.204.150')
# profile.set_preference('network.proxy.http_port', 61202)
# profile.set_preference('network.proxy.ssl', '112.116.204.150')
# profile.set_preference('network.proxy.ssl_port', 61202)

profile.update_preferences()
driver = webdriver.Firefox(profile)


url=('https://mp.weixin.qq.com/profile?src=3&timestamp=1526374356&ver=1&signature=Eu9LOYSA47p6WE0mojhMtFR-gSr7zsQOYo6*w5VxrUh3mdsgeChS825zmp*l8chPUdG3YHp-shNFGgqfdZFtdg==')
driver.get(url=url)
time.sleep(3)
page_source=driver.page_source
listmain_soup=BeautifulSoup(page_source,'lxml')
qunfa=listmain_soup.find_all('div',class_="weui_msg_card_list")
qunfa_list=BeautifulSoup(str(qunfa),'lxml')
# print(qunfa_list)
page_title=[]
page_time=[]
page_url=[]
#创建文件夹
# file=open('python6359.txt','w',encoding='utf-8')
os.mkdir('python6359')
os.getcwd()
os.chdir(r'E:\example\微信公众号爬虫\python6359')
os.getcwd()

for child in qunfa_list.div.children:
    if child!='\n':
        # print(child.find('h4',class_="weui_media_title").string)
        page_title.append(str(child.find('h4',class_="weui_media_title").string).replace('\n','').replace(' ',''))
        page_time.append(child.find('p',class_="weui_media_extra_info").string)
        #爬取，同时拼接URL
        page_url.append('https://mp.weixin.qq.com'+(child.h4.get('hrefs')))
print(page_title,'\n',page_time,'\n',page_url)
#进入每个URL爬取文章
for i in range(0,10):
    file=open(page_title[i]+'.doc','w',encoding='utf-8')
    file.write(page_title[i] + '\n')
    file.write(page_time[i] + '\n')

    download_req=request.Request(url=page_url[i])
    download_res=request.urlopen(download_req)
    download_html=download_res.read().decode('utf-8')
    soup_texts = BeautifulSoup(download_html, 'lxml')
    texts = soup_texts.find_all(id='js_content', class_='rich_media_content ')
    soup_text = BeautifulSoup(str(texts), 'lxml').text
    # write_flag = True
    soup_text=str(soup_text).replace('。','\n')
    file.write(str(soup_text))
    # for each in soup_text.text.replace('/xa0',''):
    #     if each == 'h':
    #         write_flag = False
    #     if write_flag == True and each != '':
    #         file.write(each)
    #     if write_flag == True and each == '\r':
    #         file.write('\n')
    file.write('\n\n')
    file.close()






