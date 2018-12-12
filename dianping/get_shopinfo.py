#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm

from dianping import *
import re
from bs4 import  BeautifulSoup

def get_id():
    # 从数据库获取店铺id
    cursor,conn=connect_mysql()
    shopid_sql='SELECT shopId,shopName FROM food_rank;'
    cursor.execute(shopid_sql)
    shopid_list=list(cursor.fetchall())
    shopname_list=[]
    for each in shopid_list[:]:
        shopid_list.append(each[0])
        shopname_list.append(each[1])
        shopid_list.remove(each)
    # shopid_list=set(shopid_list)
    # shopname_list=set(shopname_list)
    cursor.close()
    conn.close()
    return shopid_list,shopname_list
    # print(shopid_list,len(shopid_list))

def create_shop_db():
    cursor, conn = connect_mysql()
    sql = 'CREATE TABLE IF NOT EXISTS shop_info(' \
          'id INT UNSIGNED AUTO_INCREMENT,' \
          'shopId VARCHAR(100) NOT NULL,' \
          'shopName VARCHAR(100) NOT NULL,' \
          'review VARCHAR(3000) NULL,' \
          'review_recommend VARCHAR(300) NULL,' \
          'review_time TIMESTAMP NULL,' \
          'PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def get_shop_info():
    create_shop_db()
    shopid_list,shopname_list = get_id()
    base_url = 'http://www.dianping.com/shop/'
    for i in range(0,len(shopid_list)):
        info_url=base_url+shopid_list[i]+'/review_all'
        try:
            res=request_set(info_url)
            # good_count = res.xpath('//label[@class="filter-item filter-good"]/span/text()')[0][1:-1]
            # middle_count = res.xpath('//label[@class="filter-item filter-middle"]/span/text()')[0][1:-1]
            # bad_count = res.xpath('//label[@class="filter-item filter-bad"]/span/text()')[0][1:-1]
            # re_num = res.xpath('//span[@class="active"]/em/text()')[0][1:-1]
            pages = res.xpath('//div[@class="reviews-pages"]/a[last()-1]/text()')[0]
            tags=res.xpath('//div[@class="reviews-tags"]/div[@class="content"]//span/a/text()')
            for each in tags[:]:
                re_each=clear_text(each)
                tags.append(re_each)
                tags.remove(each)
            # print(good_count,middle_count,bad_count,re_num,pages,tags)

            get_rewiew_info(res,shopname_list[i])

            if pages>=2:
                for i in range(2,pages+1):
                    rewiew_url=info_url+'/p'+str(i)
                    res = request_set(rewiew_url)
                    get_rewiew_info(res,shopid_list[i],shopname_list[i])
        except:
            print('请求异常',pages.)


def get_rewiew_info(res,shopid,shopname):
    soup = BeautifulSoup(res, 'lxml')
    reviews = []
    recommends=[]
    review_times=[]
    try:
        soup=soup.find(class_='reviews-items').ul.find_all('li',recursive=False)
        # print(soup)
        for i in soup:
            i=BeautifulSoup(str(i),'lxml')
            # print(i,'\n\n***************************************************************************************\n\n')
            try:
                review = i.find_all(class_='review-words Hide')[0].get_text()[:-4]
            except:
                review=i.find_all(class_='review-words')[0].get_text()
            try:
                review_recommend = i.find_all('div', class_='review-recommend')[0].get_text()
                review_recommend=review_recommend.replace('\n',',').replace(' ','')[6:]
            except:
                review_recommend='无推荐菜'

            review_time = i.find_all('span', class_='time')[0].get_text()
            reviews.append(review)
            recommends.append(review_recommend)
            review_times.append(review_time)
        reviews = clear_text(reviews)
        review_times=clear_text(review_times)
        # 对time进行重新清洗
        for time in review_times[:]:
            clear_time=time[-15:]
            review_times.append(clear_time[:-5]+' '+clear_time[-5:]+':00')
            review_times.remove(time)
        # print(reviews,recommends,review_times)
        insert_review_info(reviews,recommends,review_times,shopid,shopname)

    except:
        print('fail')
        # # 后期添加tenserflow识别验证码
        # if soup.find_all('div',class_='_slider__sliderTitle___119tD') or soup.find_all('yodaModuleWrapper'):
        #     print('需要验证码\n')
        #     if input() ==1:
        #         pass
        #     # 如果是滑动验证，模拟滑动
        # else:
        #     print('页面爬取错误')

def insert_review_info(reviews,recommends,review_times,shopid,shopname):
    cursor, conn = connect_mysql()
    for i in range(0, len(reviews)):
        try:
            sql = 'INSERT INTO shop_info(shopId,shopName,review,review_recommend,review_time) VALUES(%s,%s,%s,%s,%s)'
            cursor.execute(sql,(shopid,shopname,reviews[i],recommends[i],review_times[i]))
            conn.commit()
        except:
            pass
    # 去重
    a = 'delete from shop_info where id in (select id from (select id from shop_info where id not in (select min(id) from shop_info group by review)) as temple)'
    cursor.execute(a)
    conn.commit()
    cursor.close()
    conn.close()


get_shop_info()
# text=open('test.txt',encoding='utf-8')
# create_shop_db()
# get_rewiew_info(text.read(),'111','name')