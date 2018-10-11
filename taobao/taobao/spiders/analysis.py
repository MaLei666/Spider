#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-06 12:50
# @file : analysis.py
# @software : PyCharm
import numpy as np
from pymongo import MongoClient
from  matplotlib import pyplot as plt
import re,json,jieba,pandas
from collections import Counter
from wordcloud import WordCloud
# matprotlib显示中文
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

def data_analysis(parameter):
    client = MongoClient('mongodb://admin:zkyr1006@localhost:28018')
    db = client.taobao
    colls = [db.内搭, db.外套, db.牛仔裤, db.秋季套装]
    data=[]
    for coll in colls:
        list_data=coll.aggregate([{'$group': {'_id': 0, parameter: {'$push': '$'+parameter}}}]).next()[parameter]
        data+=list_data
    return data
    # print(provience)

def provience():
    data=[]
    provs=data_analysis('area')
    # print(provience)
    for each in provs:
        prov = (each.split())[0]
        data.append(prov)
    count={}
    for i in data:
        count[i]=data.count(i)
    print(count)
    prov=list(count.keys())
    nums=list(count.values())
    return prov,nums


def cloud_data():
    title=data_analysis('title')
    titles=[]
    # 对每个标题进行分词
    for each in title:
        title_cut=jieba.lcut(each)
        titles.append(title_cut)

    # 剔除不需要的词语
    title_del=[]
    for line in titles:
        line_del=[]
        for word in line:
            if word not in ['2018','妈妈','❤','】','【',' ','Chinism','工作室','倔强']:
                line_del.append(word)
        title_del.append(line_del)
    # print(title_del)

    # 元素去重,每个标题中不含重复元素
    title_clean=[]
    for each in title_del:
        line_dist=[]
        for word in each:
            if word not in line_dist:
                line_dist.append(word)
        title_clean.append(line_dist)

    # 将所有词语转为一个list
    allwords_dist=[]
    for line in title_clean:
        for word in line:
            allwords_dist.append(word)
    # 吧列表转为数据框
    allwords_dist=pandas.DataFrame({'allwords':allwords_dist})
    # 对词语进行分类汇总
    word_count=allwords_dist.allwords.value_counts().reset_index()
    # 添加列名
    word_count.columns=['word','count']
    print(allwords_dist)
    return word_count,title_clean

def cloud():
    word_count=cloud_data()[0]
    # 设置字体，背景颜色，字体最大号，
    w_c=WordCloud(font_path='/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/simhei.ttf',
                  background_color='white',
                  max_font_size=60,
                  margin=1)
    # 取前400个词进行可视化
    wc=w_c.fit_words({x[0]:x[1] for x in word_count.head(1000).values})
    # 设置图优化
    plt.imshow(wc,interpolation='bilinear')
    # 去除边框
    plt.axis('off')
    plt.show()

# cloud()
# def cloud_data_count():
#     word_count,title_clean=cloud_data()
#     ws_count=[]
#     for each in word_count.word:
#         i=0
#         s_list=[]
#         for t in title_clean:
#             if each in t:
#                 s_list.append(data)

def plot():
    prov,nums=provience()

    plt.figure(figsize=(8,4))
    plt.xticks(rotation=0)
    plt.bar(prov,nums,color='g')
    plt.xlabel('省份')
    plt.ylabel('数量')
    plt.title('不同省份数量分布图')
    plt.legend()
    plt.show()

# plot()
