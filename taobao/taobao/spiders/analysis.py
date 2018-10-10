#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-06 12:50
# @file : analysis.py
# @software : PyCharm
import numpy as np
from pymongo import MongoClient
from  matplotlib import pyplot as plt
import re,json
from collections import Counter

def data_analysis():
    sell_count = []
    provience=[]
    client=MongoClient('mongodb://admin:zkyr1006@localhost:28018')
    db=client.taobao
    collection=db.内搭
    area=collection.aggregate([{'$group': {'_id': 0, 'area': {'$push': '$area'}}}]).next()['area']
    # print(a)
    for each in area:
        prov=(each.split())[0]
        provience.append(prov)
    return provience
    # print(provience)




def plot():
    provience=np.array(data_analysis())
    a=str(Counter(provience))[8:-1]
    
    print(a)
    # print(np.array(a))
    # plt.figure(figsize=(8,4))
    #
    # plt.xticks(rotation=0)
    # plt.xlabel('省份')
    # plt.ylabel('数量')
    # plt.title('不同省份数量分布图')
    # plt.show()












plot()
