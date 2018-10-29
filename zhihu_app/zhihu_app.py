#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-10-29 14:52
# @file : zhihu_app.py
# @software : PyCharm

import requests,json,pymysql,time

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

conn,cursor=connect_mysql()

headers = {
    'x-api-version': '3.0.89',
    'x-app-version': '5.26.2',
    'x-app-za': 'OS=Android&Release=8.0.0&Model=SM-G9500&VersionName=5.26.2&VersionCode=913&Product=com.zhihu.android&Width=1080&Height=2076&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D&DeviceType=AndroidPhone&Brand=samsung',
    'x-app-flavor': 'myapp',
    'x-app-build': 'release',
    'x-network-type': 'WiFi',
    'Host': 'api.zhihu.com',
    'User-Agent': 'com.zhihu.android/Futureve/5.26.2 Mozilla/5.0 (Linux; Android 8.0.0; SM-G9500 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
    'Connection': 'keep-alive'
}

base_url='https://api.zhihu.com/v4/questions/298905976/answers?order_by=&show_detail=1'
sql='INSERT INTO zhihu_app(question,text,author,voteup_count,comment_count,update_time)  VALUES(%s,%s,%s,%s,%s,%s)'

for i in range(0,10,5):
    params = {'offset': i}
    res = requests.get(base_url, headers=headers, params=params).json()['data']
    for each in res:
        update_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(each['updated_time']))
        item=[]
        cursor.execute(sql, (
            each['question']['title'],
            each['excerpt'],
            each['author']['name'],
            int(each['voteup_count']),
            int(each['comment_count']),
            str(update_time)
        ))
    conn.commit()

conn.close()
cursor.close()

# print items



# 可以添加一个自定义搜索的功能



# 从热榜爬取热门问题
start_url='https://api.zhihu.com/topstory/hot-list?limit=10'
res=requests.get(start_url).json()['data']
for each in res:
    hot=each['detail_text']
    title=each['target']['title']
    excerpt=each['target']['excerpt']
    answer_count=each['target']['answer_count']
    comment_count=each['target']['comment_count']
    guanzhu=each['target']['follower_count']




























