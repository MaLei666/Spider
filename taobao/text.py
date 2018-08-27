# -*- coding: utf-8 -*-
import requests

headers = {
    'Connection': 'keep-alive',
    'Host': 'www.taobao.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
url='https://s.taobao.com/list?q=牛仔裤&cat=50344007&style=grid&seller_type=taobao'
# yield SplashRequest(page_url, self.parse1, args={'wait': 0.5}, splash_headers=self.headers, dont_filter=True)
page=requests.get(url,headers=headers)
print(page.text)


