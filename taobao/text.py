# -*- coding: utf-8 -*-
import requests

headers = {
    'Connection': 'keep-alive',
    'Host': 'item.taobao.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'
}
url='https://item.taobao.com/item.htm?spm=a219r.lm874.14.1.422f2140YG82hc&id=574990577169&ns=1&abbucket=20#detail'
# yield SplashRequest(page_url, self.parse1, args={'wait': 0.5}, splash_headers=self.headers, dont_filter=True)
page=requests.get(url,headers=headers)
print(page.text)


