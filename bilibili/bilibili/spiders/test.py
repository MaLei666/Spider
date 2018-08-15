# -*- coding: utf-8 -*-
import urllib,sys
from urllib.parse import quote
string='https://www.bilibili.com/v/technology/fun/#/all/click/0/1/2018-08-01,2018-08-15'
string=quote(string)
print(string)