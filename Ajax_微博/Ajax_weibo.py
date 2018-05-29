# -*- coding: utf-8 -*-
from urllib.parse import urlencode
import requests,pymysql
from pyquery import PyQuery as pq

# 连接数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='zkyr1006',
                             db='python',
                             charset='utf8')

cursor=connection.cursor()
sql = "USE python;"
cursor.execute(sql)
connection.commit()


weibo = '''
    CREATE TABLE weibo(
        序号 INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        ID VARCHAR (255),
        text VARCHAR (255),
        attitudes VARCHAR (255),
        comments VARCHAR (255), 
        reposts VARCHAR (255) 
    )
'''


try:
    cursor.execute(weibo)
    connection.commit()
except:
    pass
# a= '''ALTER TABLE `python`.`weibo` CHANGE COLUMN `序号` `序号` INT NOT NULL AUTO_INCREMENT  ;'''
# cursor.execute(a)

base_url='https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2145291155',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# https://m.weibo.cn/api/container/getIndex?type=uid&value=2145291155&containerid=1076032145291155
# 拼接url
def get_page(page):
    # 查询字符串
    params = {
        'type': 'uid',
        'value': '2145291155',
        'containerid': '1076032145291155',
        'page': page
    }
    # 调用urlencode() 方法将params参数转化为 URL 的 GET请求参数
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.json())
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        # print(items)
        for index,item in enumerate(items):
            if page == 1 and index == 1:
                continue
            else:
                item = item.get('mblog')
                # weibo = {}
                # weibo['id'] = item.get('id')
                # weibo['text'] =
                # weibo['attitudes'] = item.get('attitudes_count')
                # weibo['comments'] = item.get('comments_count')
                # weibo['reposts'] = item.get('reposts_count')

                weibo = []
                weibo.append(item.get('id'))
                text=pq(item.get('text')).text()

                weibo.append()
                # weibo.append('无内容')
                weibo.append(item.get('attitudes_count'))
                weibo.append(item.get('comments_count'))
                weibo.append(item.get('reposts_count'))

                sql = '''INSERT IGNORE INTO weibo (ID,text,attitudes,comments,reposts)
                      VALUES (%s,%s,%s,%s,%s) on duplicate key update ID=values(ID)'''

                cursor.execute(sql,weibo)
                connection.commit()
            yield weibo

if __name__ == '__main__':
    for page in range(1, 17):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
cursor.close()
