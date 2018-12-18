#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-11-29 12:05
# @file : dianping.py
# @software : PyCharm

from datetime import datetime as dt
from dianping import *

def create_db():
    cursor, conn = connect_mysql()
    sql = 'CREATE TABLE IF NOT EXISTS food_rank(' \
          'id INT UNSIGNED AUTO_INCREMENT,' \
          'tip VARCHAR(100) NOT NULL,' \
          'tip_id INT(100) NULL,' \
          'classifi VARCHAR(100) NULL,' \
          'rank_num INT(100) NULL,' \
          'shopId VARCHAR(100) NOT NULL,' \
          'shopName VARCHAR(100) NOT NULL,' \
          'mainRegionName VARCHAR(100) NULL,' \
          'taste FLOAT(10) NULL,' \
          'environment FLOAT(10) NULL,' \
          'service FLOAT(10) NULL,' \
          'avgPrice INT(255) NULL,' \
          'city_id INT(100) NULL,' \
          'address VARCHAR(100) NULL,' \
          'update_time DATE NULL,' \
          'PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def insert_db(classifi,class_name):
    cursor, conn = connect_mysql()
    update_time = dt.now().date()

    for i in range(0, len(classifi)):
        # print(classifi[i],class_name[i])
        num = 1
        # 获取分类排行榜的信息
        data = requests.get(url=classifi[i], headers=headers).json()
        shopdata = data['shopBeans']
        cityid = data['cityId']
        try:
            # 保存每个商铺的信息
            for each in shopdata:
                mainCategoryName = each['mainCategoryName']
                shopName = each['shopName']
                branchName = each['branchName']
                if len(branchName) != 0:
                    shopName = shopName + '(' + branchName + ')'
                shopId = each['shopId']
                mainRegionName = each['mainRegionName']
                taste = each['refinedScore1']
                environment = each['refinedScore2']
                service = each['refinedScore3']
                avgPrice = each['avgPrice']
                address = each['address']
                sql = 'INSERT INTO food_rank(tip,tip_id,classifi,rank_num,shopId,shopName,mainRegionName,taste,environment,service,avgPrice,city_id,address,update_time) ' \
                      'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (class_name[i],
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
                                     cityid,
                                     address,
                                     update_time))
                conn.commit()
                num += 1
            print('爬取{}排行榜成功'.format(class_name[i]))
        except:
            print('获取商铺信息出错')
    # 去重
    a = 'delete from food_rank where id in (select id from (select id from food_rank where id not in (select min(id) from food_rank group by class,shopName,rank_num)) as temple)'
    cursor.execute(a)
    conn.commit()
    cursor.close()
    conn.close()

def get_rank_info():
    create_db()
    base_url = 'http://www.dianping.com'
    start_url = 'http://www.dianping.com/beijing/food'
    try:
        res = requests.get(start_url, headers=headers).text
        response = etree.HTML(res)
        hot_url = response.xpath('//div[@class="item news_list current"]/a[@class="more"]/@href')
        # print(hot_url)
        classifi_res = requests.get((base_url + hot_url[0]), headers).text
        response = etree.HTML(classifi_res)
        # 第一行标签
        classifi1 = hot_url + response.xpath('//div[@class="box shopRankNav"]/p[1]//a/@href')
        class_name1 = ['热门'] + response.xpath('//div[@class="box shopRankNav"]/p[1]//a/text()')
        # 第二行标签
        classifi2 = response.xpath('//div[@class="box shopRankNav"]/p[2]//a/@href')
        class_name2 = response.xpath('//div[@class="box shopRankNav"]/p[2]//a/text()')
        # 所有标签和名称
        class_name = class_name1 + class_name2
        classifi = classifi1 + classifi2
        ajax_base_url = 'http://www.dianping.com/mylist/ajax/shoprank?rankId='
        for each in classifi[:]:
            classifi.append(ajax_base_url + each.split('=')[1])
            classifi.remove(each)
        insert_db(classifi,class_name)
    except:
        print('爬取榜单出错')

get_rank_info()










