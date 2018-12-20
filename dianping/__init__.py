

__all__=['connect_mysql','browser_set','headers','get_proxy','requests','conf','etree','sleep','request_set','clear_text','remove_emoji']

import pymysql,requests,random,re
from selenium import webdriver
from configparser import ConfigParser
from lxml import etree
from time import sleep
# from fake_useragent import UserAgent
# ua = UserAgent(use_cache_server=False,verify_ssl=False)

conf = ConfigParser()
conf.read('conf.ini')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
           'Cookie': '{}={}'.format(conf.get('cookies','name'),conf.get('cookies','value')),
           'Referer': 'http://www.dianping.com/shop/102474045/review_all',
           'Connection': 'keep-alive',
           'Host': 'www.dianping.com',
           }

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

'''
代理启动步骤
cd /home/py_code/spider/
pipenv shell
cd proxy_pool/Run
python main.py
'''
def get_proxy():
    return requests.get("http://192.168.1.137:8001/get/").text

def remove_emoji(text):
    try:
        Emoji=re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        Emoji = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return Emoji.sub(u'\u25FD',text)

def clear_text(input):
    for each in input[:]:
        re_each = re.sub('\n+', '', each)
        re_each = re.sub(' +', '', re_each)
        re_each = re.sub('\t+', '', re_each)
        re_each = re.sub('\xa0', '', re_each)
        re_each = re.sub(r'[^\u4e00-\u9fa5]', '', re_each)
        re_each = remove_emoji(re_each)
        re_each = re.sub('收起评论', '', re_each)
        input.append(re_each)
        input.remove(each)
    while '' in input:
        input.remove('')
    return input


# request请求设置
def request_set(req_url):
    sleep(random.random() * 6 + 2)
    try:
        res = requests.get(url=req_url,timeout=10, headers=headers)
        res.raise_for_status()
        res.encoding = 'utf-8'
        return res.text
    except:
        print('请求网页失败')

def browser_set():
    # 火狐
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    browser=webdriver.Firefox(options=options)

    # 设置代理
    # service_args = [
    #     # '--proxy=%s' %get_proxy(), # 代理 IP：prot    （eg：192.168.0.28:808）
    #     # '--ssl-protocol=any', #忽略ssl协议
    #     # '--load - images = no', # 关闭图片加载（可选）
    #     # '--disk-cache=yes', # 开启缓存（可选）
    #     # '--ignore-ssl-errors=true' # 忽略https错误(可选)
    # ]

    # 谷歌
    # options=webdriver.ChromeOptions()
    # # options.add_argument('--headless')
    # browser=webdriver.Chrome(options=options)

    # PhantomJS
    # from selenium.webdriver import DesiredCapabilities
    # user_Agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = user_Agent
    # browser=webdriver.PhantomJS(desired_capabilities=dcap)
    return browser


