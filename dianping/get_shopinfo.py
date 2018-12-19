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
            page = info[1]
            re_no = info[2]
            if re_no==19:
                page+=1
                re_no=0
                print('断点开始处为：{}-第{}页-第{}条评论'.format(shopname_list[0], page, re_no+1))
            else:
                re_no+=1
                print('断点开始处为：{}-第{}页-第{}条评论'.format(shopname_list[0],page,re_no))
            return shopid_list, shopname_list, page, re_no
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

def verify_page(soup,url):
    # 判断是否为验证码
    # 后期添加tenserflow识别验证码，如果是滑动验证，模拟滑动
    if soup.find(text='验证中心') or soup.find(text='很抱歉，您要访问的页面不存在'):
        # print(soup)
        print('需要验证\n')
        if input() == 1:
            print('验证成功')
        res=request_set(url)
        res=BeautifulSoup(res, 'lxml')
        return res
    else:
        return soup

def insert_review_info(reviews,recommends,review_times,shopid,shopname,page):
    cursor, conn = connect_mysql()
    update_time=dt.now()
    for i in range(0, len(reviews)):
        try:
            sql = 'INSERT INTO shop_info(shopId,shopName,review,review_recommend,review_time,update_time,' \
                  'now_page,re_no) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(shopid,shopname,reviews[i],recommends[i],review_times[i],update_time,
                                str(page),str(i)))
            conn.commit()
        except:
            print('信息入库失败')
            conn.rollback()
    cursor.close()
    conn.close()

def get_review_info(res,page,re_no,shopid,shopname,url):
    soup = BeautifulSoup(res, 'lxml')
    reviews = []
    recommends=[]
    review_times=[]
    # 设置评论开始点，默认从第1条，存在断点第话取断点值
    begin_point=0
    if re_no!=0:
        begin_point=re_no+1

    try:
        soup=verify_page(soup,url)
        # 查找所有评论的标签
        soup=soup.find(class_='reviews-items').ul.find_all('li',recursive=False)
        soup=soup[begin_point:]
        for i in soup:
            i=BeautifulSoup(str(i),'lxml')
            try:
                review = i.find_all(class_='review-words Hide')[0].get_text()[:-7]
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
        return page
    except:
        print('页面爬取失败')

def get_shop_info():
    create_shop_db()
    # 获取店铺信息，和断点信息
    shopid_list,shopname_list,now_page,re_no = get_id()
    base_url = 'http://www.dianping.com/shop/'
    # 遍历店铺
    for i in range(0,len(shopid_list)):
        # 开始爬取页码默认设置为1
        begin_page=1
        info_url=base_url+shopid_list[i]+'/review_all'
        try:
            res=request_set(info_url)
            # res_html = etree.HTML(res)
            res_html=BeautifulSoup(res,'lxml')
            # good_count = res.xpath('//label[@class="filter-item filter-good"]/span/text()')[0][1:-1]
            # middle_count = res.xpath('//label[@class="filter-item filter-middle"]/span/text()')[0][1:-1]
            # bad_count = res.xpath('//label[@class="filter-item filter-bad"]/span/text()')[0][1:-1]
            # re_num = res.xpath('//span[@class="active"]/em/text()')[0][1:-1]
            # tags=res_html.xpath('//div[@class="reviews-tags"]/div[@class="content"]//span/a/text()')
            # tags=clear_text(tags)
            # print(good_count,middle_count,bad_count,re_num,pages,tags)
            try:
                res=verify_page(res_html,info_url)
                # 小于1页的没有page元素，默认不爬取
                pages=int(res.find(class_='reviews-pages').find_all('a')[-2].get_text())
                # pages = int(res_html.xpath('//div[@class="reviews-pages"]/a[last()-1]/text()')[0])
                # 如果返回的当前页码为0，即从未爬取过，或者为每次的新商户爬取。设置开始页码为2
                if now_page==0:
                    begin_page=2
                    # 爬取第一页
                    try:
                        get_review_info(res, 1, 0, shopid_list[i], shopname_list[i],info_url)
                    except:
                        break
                # 如果返回的当前页码不为0，即存在断点，从断点处续爬
                elif now_page!=0:
                    begin_page=now_page

                # 爬取第二页或者指定页到尾页
                while begin_page<=pages:
                    try:
                        for page in range(begin_page, pages + 1):
                            review_url = info_url + '/p' + str(page)
                            # print(review_url)
                            res = request_set(review_url)
                            page=get_review_info(res, page, re_no,shopid_list[i], shopname_list[i],info_url)
                            begin_page=page+1
                        print('爬取{}店铺成功'.format(shopname_list[i]))
                    except:
                        print('爬取{}店铺失败'.format(shopname_list[i]))
                        break
                    # 每次爬取一个店铺完毕，将nowpage和reno置0，防止每个店铺都存在断点
                    finally:
                        now_page=0
                        re_no=0
            except:
                print('店铺评论小于一页，跳过爬取')
                break
        except:
            print('请求失败')
            break
    print('爬取结束')

get_shop_info()


