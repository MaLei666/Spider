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
# matprotlib显示中文
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

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

def check():
    provience=data_analysis()
    a={}
    for i in provience:
        a[i]=provience.count(i)
    prov=list(a.keys())
    nums=list(a.values())
    return prov,nums

def plot():
    prov,nums=check()

    plt.figure(figsize=(8,4))
    plt.xticks(rotation=0)
    plt.bar(prov,nums,color='g')
    plt.xlabel('省份')
    plt.ylabel('数量')
    plt.title('不同省份数量分布图')
    plt.legend()
    plt.show()

plot()
