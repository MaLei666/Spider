#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-11-29 12:05
# @file : dianping.py
# @software : PyCharm

import requests,pymysql,re
from bs4 import BeautifulSoup
from lxml import etree
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
base_url='http://www.dianping.com'
start_url='http://www.dianping.com/beijing/food'
res=requests.get(start_url,headers=headers).text
response=etree.HTML(res)
hot_url=response.xpath('//div[@class="item news_list current"]/a[@class="more"]/@href')
# print(hot_url)
classifi_res=requests.get((base_url+hot_url[0]),headers).text
response=etree.HTML(classifi_res)

classifi1=hot_url+response.xpath('//div[@class="box shopRankNav"]/p[1]//a/@href')
class_name1=['热门']+response.xpath('//div[@class="box shopRankNav"]/p[1]//a/text()')

classifi2=response.xpath('//div[@class="box shopRankNav"]/p[2]//a/@href')
class_name2=response.xpath('//div[@class="box shopRankNav"]/p[2]//a/text()')

class_name=class_name1+class_name2
classifi=classifi1+classifi2
ajax_base_url='http://www.dianping.com/mylist/ajax/shoprank?rankId='

for each in classifi[:]:
    classifi.append(ajax_base_url+each.split('=')[1])
    classifi.remove(each)
# print(classifi,len(classifi))
cursor,conn=connect_mysql()
sql = 'CREATE TABLE IF NOT EXISTS food_rank(' \
      'id INT UNSIGNED AUTO_INCREMENT,' \
      'class VARCHAR(100) NOT NULL,' \
      'classifi VARCHAR(100) NULL,' \
      'class_id int(100) NULL,' \
      'rank int(100) NULL,' \
      'shopId VARCHAR(100) NOT NULL,' \
      'shopName VARCHAR(100) NOT NULL,' \
      'mainRegionName VARCHAR(100) NULL,' \
      'taste float(10) NULL,' \
      'environment float(10) NULL,' \
      'service float(10) NULL,' \
      'avgPrice int(255) NULL,' \
      'address VARCHAR(100) NULL,' \
      'PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
cursor.execute(sql)
conn.commit()
for i in range(0,len(classifi)):
    print(classifi[i],class_name[i])
    num=1
    data=requests.get(url=classifi[i],headers=headers).json()['shopBeans']
    try:
        for each in data:
            mainCategoryName=each['mainCategoryName']
            shopName=each['shopName']
            branchName=each['branchName']
            if len(branchName)!=0:
                shopName=shopName+'('+branchName+')'
            shopId=each['shopId']
            mainRegionName=each['mainRegionName']
            taste=each['refinedScore1']
            environment=each['refinedScore2']
            service=each['refinedScore3']
            avgPrice=each['avgPrice']
            address=each['address']
            sql='INSERT INTO food_rank(class,class_id,classifi,rank,shopId,shopName,mainRegionName,taste,environment,service,avgPrice,address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(class_name[i],
                                i,
                                mainCategoryName,
                                num,
                                shopId,
                                shopName,
                                mainRegionName,
                                taste,
                                environment,
                                service,
                                avgPrice,
                                address))
            conn.commit()
            num+=1
    except:
        pass

# 去重
a='delete from food_rank where id in (select id from (select id from food_rank where id not in (select min(id) from food_rank group by class,shopName,rank)) as temple)'
cursor.execute(a)
conn.commit()

cursor.close()
conn.close()

# cursor,conn=connect_mysql()
# shopname_sql='SELECT shopName FROM food_rank'
# cursor.execute(shopname_sql)
# shopname=cursor.fetchall()
# shop_list=[]
# for each in shopname:
#     shop_list.append(each[0])
# shop_list=list(set(shop_list))
# # print(shop_list,len(shop_list))
# for shop in shop_list:



















