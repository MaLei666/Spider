#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-12-06 13:54
# @file : get_shopinfo.py
# @software : PyCharm

from dianping import *
import re
from bs4 import  BeautifulSoup
from datetime import datetime as dt

def get_id():
    # 续爬功能查询断点处
    def begin_point(shopid_list, shopname_list):
        # 查询是哪个商铺的第几页的第几条评论
        check_db_sql = 'select shopId,now_page,re_no from shop_info order by id DESC limit 1'
        cursor.execute(check_db_sql)
        info = cursor.fetchone()
        try:
            list_id = shopid_list.index(info[0])
            shopid_list = shopid_list[list_id:]
            shopname_list=shopname_list[list_id:]
            return shopid_list, shopname_list, info[1], info[2]
        except:
            return shopid_list, shopname_list, 0, 0

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
    shopid_list,shopname_list,now_page,re_no=begin_point(shopid_list,shopname_list)
    cursor.close()
    conn.close()
    return shopid_list,shopname_list,now_page,re_no

def create_shop_db():
    try:
        cursor, conn = connect_mysql()
        sql = 'CREATE TABLE IF NOT EXISTS shop_info(' \
              'id INT UNSIGNED AUTO_INCREMENT,' \
              'shopId VARCHAR(100) NOT NULL,' \
              'shopName VARCHAR(100) NOT NULL,' \
              'review VARCHAR(3000) NULL,' \
              'review_recommend VARCHAR(300) NULL,' \
              'review_time TIMESTAMP NULL,' \
              'update_time TIMESTAMP NULL,' \
              'now_page INT NOT NULL ,' \
              're_no INT NOT NULL, '\
              'PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        print('shop_info表创建成功')
    except:
        print('创建失败')

def get_shop_info():
    create_shop_db()
    shopid_list,shopname_list,now_page,re_no = get_id()
    base_url = 'http://www.dianping.com/shop/'
    for i in range(0,len(shopid_list)):
        begin_page=0
        info_url=base_url+shopid_list[i]+'/review_all'
        pages=0
        try:
            res=request_set(info_url)
            res_html = etree.HTML(res)
            # good_count = res.xpath('//label[@class="filter-item filter-good"]/span/text()')[0][1:-1]
            # middle_count = res.xpath('//label[@class="filter-item filter-middle"]/span/text()')[0][1:-1]
            # bad_count = res.xpath('//label[@class="filter-item filter-bad"]/span/text()')[0][1:-1]
            # re_num = res.xpath('//span[@class="active"]/em/text()')[0][1:-1]
            # tags=res_html.xpath('//div[@class="reviews-tags"]/div[@class="content"]//span/a/text()')
            # tags=clear_text(tags)
            # print(good_count,middle_count,bad_count,re_num,pages,tags)
            try:
                # 小于1页的没有page元素
                pages = int(res_html.xpath('//div[@class="reviews-pages"]/a[last()-1]/text()')[0])
                if now_page==0:  #第一次爬取/断点后新商户爬取
                    begin_page=2
                elif now_page!=0:   #有断点的爬取
                    begin_page=now_page
                # 爬取第一页
                try:
                    get_rewiew_info(res, 1, shopid_list[i], shopname_list[i])
                except:
                    break
                # 爬取第二页或者指定页到尾页
                for page in range(begin_page, pages + 1):
                    # 判断为第几条
                    if re_no


                    review_url = info_url + '/p' + str(page)
                    res = request_set(review_url)
                    try:
                        get_rewiew_info(res, page, shopid_list[i], shopname_list[i])
                    except:
                        break
                print('爬取{}店铺成功'.format(shopname_list[i]))
            except:
                print('店铺评论小于一页，跳过爬取')




        except:
            break


def get_rewiew_info(res,page,shopid,shopname):
    soup = BeautifulSoup(res, 'lxml')
    reviews = []
    recommends=[]
    review_times=[]
    try:
        soup=soup.find(class_='reviews-items').ul.find_all('li',recursive=False)
        for i in soup:
            i=BeautifulSoup(str(i),'lxml')
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
        insert_review_info(reviews,recommends,review_times,shopid,shopname,page)
        print('爬取{}第{}页成功'.format(shopname,page))

    except:
        # 后期添加tenserflow识别验证码
        # print(soup)
        if soup.find_all(class_='_slider__sliderTitle___119tD') or soup.find_all(id='not-found-tip') :
            print('需要验证\n')
            if input() ==1:
                pass
            # 如果是滑动验证，模拟滑动
        else:
            print('页面返回非评论页面')

def insert_review_info(reviews,recommends,review_times,shopid,shopname,page):
    cursor, conn = connect_mysql()
    update_time=dt.now()
    for i in range(0, len(reviews)):
        try:
            sql = 'INSERT INTO shop_info(shopId,shopName,review,review_recommend,review_time,update_time,now_page,re_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(shopid,shopname,reviews[i],recommends[i],review_times[i],update_time,str(page),str(i)))
            conn.commit()
        except:
            print('信息入库失败')
            conn.rollback()
    cursor.close()
    conn.close()

def check_db_info():
    cursor, conn = connect_mysql()
    # 去重
    a = 'delete from shop_info where id in (select id from (select id from shop_info where id not in (select min(id) from shop_info group by review)) as temple)'
    cursor.execute(a)
    conn.commit()

# get_shop_info()
