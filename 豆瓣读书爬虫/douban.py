# -*- coding: utf-8 -*-
import requests,time,pymysql,re,random,xlwt
from bs4 import BeautifulSoup
pymysql.install_as_MySQLdb()
from selenium import webdriver

# 连接数据库
connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             passwd='zkyr1006',
                             db='python',
                             charset='utf8')

cursor=connection.cursor
sql = "USE python;"
cursor.execute(sql)
connection.commit()

# def cookie_get():
#     #保存cookie到文件
#     filecook='cookie.txt'
#     # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
#     cookie=cookiejar.MozillaCookieJar(filecook)
#     # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
#     handler=request.HTTPCookieProcessor(cookie)
#     # 通过CookieHandler创建opener
#     opener=request.build_opener(handler)
#     res=opener.open('https://book.douban.com/')
#     # ignore_discard的意思是即使cookies将被丢弃也将它保存下来；
#     # ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
#     cookie.save(ignore_discard=True,ignore_expires=True)



def login(url):
# 文件中获取cookie并访问
    cookies={}
    s = requests.session()
    with open('E:\example\豆瓣读书爬虫\cookie.txt')as file:
        raw_cookies=file.read()
        for line in raw_cookies.split(';'):
            key,value=line.split('=',1)
            cookies[key]=value
    proxie = {'http': 'http://112.228.161.185:8118'}
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    res=s.get(url=url,cookies=cookies,headers=headers,proxies=proxie)
    return res

def sorturl():
    url='https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    # url='http://www.whatismyip.com.tw/'
    web=login(url)
    # print(web.text)
    urls=[]
    soup=BeautifulSoup(web.text,'lxml')
    #通过id名和子标签进行查找,>前后要有空格，不然失效
    tags=soup.select('#content > div > div.article > div > div > table > tbody > tr > td > a')
    # print(tags)
    for tag in tags:
        tag=tag.string
        tag_url='https://book.douban.com/tag/'+str(tag)
        urls.append(tag_url)
    # print(urls)
    # 连接存入
    with open('sort_artical.txt','w') as file:
        for link in urls:
            file.write(link+'\n')
    return urls
# sorturl()

#爬取书籍详细信息
def book_info():
    urls=sorturl()
    #进入每个分类的书籍列表
    for url in urls:
        #存放每一本书的数据
        data=[]
        booklist=login(url.strip())
        soup=BeautifulSoup(booklist.text.encode('utf-8'),'lxml')
        books=soup.select('''#subject_list > ul > li > div.info > h2 > a''')

        #获取每本书信息
        for book in books:
            book_url=book.get('href')
            book_data=login(book_url)

            booksoup=BeautifulSoup(book_data.text.encode('utf-8'),'lxml')

            info=booksoup.select('#info')  #select返回为列表
            #将返回的列表做处理
            if len(info)!=0:
                infos = list(info[0].strings)
                for i in range(len(infos)):
                    infos[i]=infos[i].replace(' ','').replace('\n','').replace('\xa0','')
                for each in infos:
                    if each=='':
                        infos.remove('')
                # print(infos)
                try:
                    title=booksoup.select('#wrapper > h1 > span')[0].string.replace('\n','')
                    author=booksoup.select('#info > a')[0].string.replace(' ','').replace('\n','')
                    money = infos[infos.index('定价:') + 1]
                    # index输出关键字在字符串中出现的位置，从0开始
                    publish=infos[infos.index('出版社:')+1] #输出出版社后面的一个字符串，为出版公司
                    pages = infos[infos.index('页数:') + 1]
                    years = infos[infos.index('出版年:') + 1]
                    ISBN = infos[infos.index('ISBN:') + 1]
                    people = booksoup.select('#interest_sectl > div > div > div > div > span > a > span')[0].string
                    score = booksoup.select('#interest_sectl > div > div > strong')[0].string
                except:
                    title = booksoup.select('#wrapper > h1 > span')[0].string.replace('\n', '')
                    try:
                        author = booksoup.select('#info > span > a')[0].string.replace(' ', '').replace('\n', '')
                    except:
                        author=''
                    try:
                        money = infos[infos.index('定价:') + 1]
                    except:
                        money=''
                    # index输出关键字在字符串中出现的位置，从0开始
                    try:
                        publish = infos[infos.index('出版社:') + 1]  # 输出出版社后面的一个字符串，为出版公司
                    except:
                        publish=''
                    try:
                        pages = infos[infos.index('页数:') + 1]
                    except:
                        pages=''
                    try:
                        years = infos[infos.index('出版年:') + 1]
                    except:
                        years=''
                    try:
                        ISBN = infos[infos.index('ISBN:') + 1]
                    except:
                        ISBN=''
                    try:
                        people = booksoup.select('#interest_sectl > div > div > div > div > span > a > span')[0].string
                    except:
                        people=''
                    try:
                        score = booksoup.select('#interest_sectl > div > div > strong')[0].string
                    except:
                        score=''

                eachdata=[title,author,money,publish,pages,years,ISBN,people,score]
                print(eachdata)
                data.append(eachdata)
            elif len(info) == 0:
                continue
            else:
                continue
            #存入数据库
        try:
            with connection.cursor() as cursor:
                sql = '''INSERT IGNORE INTO douban_books (title,author,money,publish,pages,years,ISBN,people,score)
                 values (%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update title=values(title)'''
                cursor.executemany(sql, data)
                connection.commit()
                del data
                time.sleep(random.randint(0, 9))  # 防止IP被封
        except:
            continue

        #程序运行时间太长，规定数据库条数，迅速看到结果
        # cursor = connection.cursor()
        # count = cursor.execute('select * from douban_books')
        # if count>=60:
        #     break

def export(table_name):
    cursor = connection.cursor()
    count = cursor.execute('select * from '+table_name)
    # print(self._cursor.lastrowid)
    print(count)
    # 重置游标的位置
    cursor.scroll(0, mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()

    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook(encoding = 'uft-8')

    # 注意: 在add_sheet时, 置参数cell_overwrite_ok=True, 可以覆盖原单元格中数据。
    # cell_overwrite_ok默认为False, 覆盖的话, 会抛出异常.
    sheet = workbook.add_sheet('table_'+table_name, cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(results)+1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row-1][col])
    workbook.save(table_name+'.xls')


start = time.clock()
# 获取书籍信息，存入数据库
book_info()
#删除重复数据，并且重新排序
cursor = connection.cursor()
a='''delete from douban_books where id in (select id from (select id from douban_books where id not in (select min(id) from douban_books group by title)) as temple);'''
cursor.execute(a)
connection.commit()
# 删除原有主键：
a='''ALTER  TABLE  `douban_books` DROP `id`;'''
cursor.execute(a)
connection.commit()
# 添加新主键字段：
a='''ALTER  TABLE  `douban_books` ADD `id` MEDIUMINT( 8 ) NOT NULL  FIRST;'''
cursor.execute(a)
connection.commit()
# 设置新主键：
a='''ALTER  TABLE  `douban_books` MODIFY COLUMN  `id` MEDIUMINT( 8 ) NOT NULL  AUTO_INCREMENT,ADD PRIMARY  KEY(id)'''
cursor.execute(a)
connection.commit()

end = time.clock()
with connection.cursor() as cursor:
    print("Time Usage:", end -start)
    count = cursor.execute('SELECT * FROM douban_books')
    print("Total of books:", count)


export('douban_books')

if connection.open:
    connection.close()



