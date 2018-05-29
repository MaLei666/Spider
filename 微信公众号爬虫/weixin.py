# -*- coding: utf-8 -*-
import requests,random,re,time,os
from urllib import request
from lxml import etree
import subprocess as sp
from selenium import webdriver
from bs4 import BeautifulSoup

def get_proxys(page=1):
    #自动保持cookie,不需要自己维护cookie内容
    s = requests.Session()
    #高匿ip地址
    url='http://www.xicidaili.com/nn/%d' %page
    #完善header
    header= {'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    }
    #get请求，应答解码
    response=s.get(url=url,headers=header)
    response.encoding='utf-8'
    #获取网页信息
    html=response.text
    #获取id为ip_list的table
    bf1=BeautifulSoup(html,'lxml')
    bf2=BeautifulSoup(str(bf1.find_all(id="ip_list")),'lxml')
    iplist=bf2.table.contents
    #存储代理列表
    global proxy_list
    proxy_list=[]
    #爬取每个代理的信息
    for index in range(len(iplist)):
        #空行与有用数据交替，第一个元素为空行
        if index%2==1 and index!=1:
            dom=etree.HTML(str(iplist[index]))
            ip=dom.xpath('//td[2]')
            port=dom.xpath('//td[3]')
            protocol=dom.xpath('//td[6]')
            proxy_list.append(protocol[0].text.lower()+'#'+ip[0].text+'#'+port[0].text)
    return proxy_list
    #返回代理列表

'''
检查代理ip连通性
ip——代理ip地址
losetime——匹配丢包数
wastetime——匹配平均时间
average_time——代理ip平均耗时
'''
def check_ip(ip,losetime,wastetime):
    # 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd="ping -n 3 -w 3 %s"
    #执行命令
    p=sp.Popen(cmd % ip,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
    #获得返回信息并解码
    out=p.stdout.read().decode('gbk')
    #丢包数
    losetime=losetime.findall(out)
    #当匹配到丢包信息失败，默认为三次请求全部丢包，丢包数目lose赋值为3
    if len(losetime)==0:
        lose=3
    else:
        lose=int(losetime[0])
    #如果丢包数目大于2，认为连接超时，返回平均耗时1000ms
    if lose>2:
        #返回false
        return 1000
    #如果丢包数目小于等于2，获取平均耗时时间
    else:
        #平均时间
        average=wastetime.findall(out)
        #当匹配耗时时间信息失败，默认三次请求严重超时，返回平均耗时1000ms
        if len(average)==0:
            #返回false
            return 1000
        else:
            average_time=int(average[0])
            return average_time
'''
初始化正则表达式
losetime——匹配丢包数
wastetime——匹配平均时间
'''
def initpattern():
    #匹配丢包数，平均时间
    #丢失，平均的格式要和接收数据包格式一样，等号前后有空格，不然匹配不上
    losetime=re.compile(u"丢失 = (\d+)", re.IGNORECASE)
    wastetime=re.compile(u"平均 = (\d+)ms",re.IGNORECASE)
    return losetime,wastetime

def proxylist():
    losetime, wastetime = initpattern()
    # proxy_list=proxy_choose()
    while True:
        global proxy_list
        if len(proxy_list)<=20:
            proxy_list = get_proxys(1)
        else:
            # 从代理ip池中随机选取一个ip作为代理访问
            proxy = random.choice(proxy_list)
            split_proxy = proxy.split('#')
            # 获取ip
            ip = split_proxy[1]
            port=int(split_proxy[2])
            # 检查ip连通性
            average_time = check_ip(ip, losetime, wastetime)
            if average_time > 200:
                # 去掉不能使用的ip
                print(ip, '连接失败，重新获取')
                proxy_list.remove(proxy)
            if average_time < 200:
                break
    # 去掉已经使用的ip
    proxy_list.remove(proxy)
    proxy_dict = {split_proxy[1] + ':' + split_proxy[2]}
    print('使用代理：', proxy_dict,'代理池剩余ip',len(proxy_list))

    # 使用代理ip访问网址
    # 谷歌浏览器设置代理ip
    # browser = webdriver.ChromeOptions()
    # # browser.add_argument('--proxy-server=http://' + ip)
    # browser.add_argument('--proxy-server=http://223.241.78.194:8010')
    # browser.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"')
    # os.environ["webdriver.chrome.driver"] = chromedriver
    # driver = webdriver.Chrome(chromedriver, chrome_options=chome_options)

    # 火狐设置代理ip
    webdriver.DesiredCapabilities.FIREFOX[
        'firefox.page.settings.userAgent'] = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)  # 默认值0，就是直接连接；1就是手工配置代理。
    profile.set_preference('network.proxy.http', ip)
    profile.set_preference('network.proxy.http_port', port)
    profile.set_preference('network.proxy.ssl', ip)
    profile.set_preference('network.proxy.ssl_port', port)

    # profile.set_preference('network.proxy.http', '1.199.210.95')
    # profile.set_preference('network.proxy.http_port', 61234)
    # profile.set_preference('network.proxy.ssl', '1.199.210.95')
    # profile.set_preference('network.proxy.ssl_port', 61234)

    profile.update_preferences()
    driver = webdriver.Firefox(profile)
    return driver

#判断是否为错误网页
def falsepage():
    try:
        driver.get(url=URL)
        time.sleep(3)
        b = False
    except:
        # 判断是否为错误网页
        driver.find_element_by_id('errorPageContainer')
        b = True
    return b

#搜索公众号
def searchnum():
    # 获取输入框，输入英文微信公众号，搜索显示
    elem1_value = driver.find_element_by_name('query')
    elem1_value.send_keys('python6359')
    time.sleep(1)
    elem2 = driver.find_element_by_xpath('''//*[@class="querybox"]/input[@class="swz2"]''')
    elem2.click()

#进入公众号
def mainpage():
    time.sleep(2)
    mainpage=driver.find_element_by_xpath('''//*[@class="tit"]/a[1]''')
    mainpage.click()
    time.sleep(10)

    # 点击公众号，有可能出现验证码界面，页面为新跳转的页面
    handles = driver.window_handles
    driver.switch_to_window(handles[1])
    print(handles)
    time.sleep(3)

    #判断是否为验证码界面
    try:
        driver.find_element_by_id('verify_change')
        a = True
    except:
        a = False

    # 如果有这个元素，则出现了验证码界面
    if a == True:
        num = input('输入验证码:')
        number = driver.find_element_by_id('input')
        number.send_keys(num)

        time.sleep(3)
        enter = driver.find_element_by_xpath('''//*[@class="weui_btn_area btn_box"]/a[@id="bt"]''')
        enter.click()
    elif a == False:
        time.sleep(1)


#如果出现代理服务器拒绝连接，从ip池随机选择一个ip
def download():
    # 下载文章
    page_source = driver.page_source
    listmain_soup = BeautifulSoup(page_source, 'lxml')
    qunfa = listmain_soup.find_all('div', class_="weui_msg_card_list")
    qunfa_list = BeautifulSoup(str(qunfa), 'lxml')
    # print(qunfa_list)
    page_title = []
    page_time = []
    page_url = []
    # 创建文件夹
    # file=open('python6359.txt','w',encoding='utf-8')
    os.mkdir('python6359')
    os.getcwd()
    os.chdir(r'E:\example\微信公众号爬虫\python6359')
    os.getcwd()

    for child in qunfa_list.div.children:
        if child != '\n':
            # print(child.find('h4',class_="weui_media_title").string)
            page_title.append(
                str(child.find('h4', class_="weui_media_title").string).replace('\n', '').replace(' ', ''))

            page_time.append(child.find('p', class_="weui_media_extra_info").string)
            # 爬取，同时拼接URL
            page_url.append('https://mp.weixin.qq.com' + (child.h4.get('hrefs')))
    print(page_title, '\n', page_time, '\n', page_url)
    # 进入每个URL爬取文章
    for i in range(0, 10):
        file = open(page_title[i] + '.doc', 'w', encoding='utf-8')
        file.write(page_title[i] + '\n')
        file.write(page_time[i] + '\n')

        download_req = request.Request(url=page_url[i])
        download_res = request.urlopen(download_req)
        download_html = download_res.read().decode('utf-8')
        soup_texts = BeautifulSoup(download_html, 'lxml')
        texts = soup_texts.find_all(id='js_content', class_='rich_media_content ')
        soup_text = BeautifulSoup(str(texts), 'lxml').text
        # write_flag = True
        soup_text = str(soup_text).replace('。', '\n\n')
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
    driver.quit()

if __name__ == '__main__':
    URL = ('http://weixin.sogou.com/')
    #定义代理ip池列表
    proxy_list=[]
    # URL=('http://www.whatismyip.com.tw/')
    # 使用代理ip打开网页
    driver=proxylist()
    #判断是否为错误网页
    c=falsepage()
    while True:
        if c == True:
            time.sleep(1)
            driver.quit()
            #代理池中抽取ip，driver更新
            driver=proxylist()
            c=falsepage()
            if c == False:
                break
        elif c == False:
            break
    searchnum()
    time.sleep(2)
    # 查看本机ip
    # driver.get("http://httpbin.org/ip")
    # driver.maximize_window()
    # driver.quit()

    #出现验证码界面
    #判定界面有没有name=c的元素存在
    try:
        driver.find_element_by_name('c')
        a=True
    except:
        a=False
    #如果有这个元素，则出现了验证码界面
    if a==True:
        # 验证码识别
        time.sleep(10)
        mainpage()
        # 判断是否验证码输错
        # try:
        #     driver.find_element_by_name('c')
        #     a = True
        # except:
        #     a = False
        # if a == True:
        #     checknum()
        #     time.sleep(1)
        # elif a == False:
        #     time.sleep(2)
        #     mainpage()
        #     time.sleep(2)
    #如果没有这个元素，则直接出现了公众号列表
    elif a==False:
        time.sleep(2)
        mainpage()
    download()








