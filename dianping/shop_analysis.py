#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-12-19 16:35
# @file : shop_analysis.py
# @software : PyCharm

from dianping import *
import numpy as np
from  matplotlib import pyplot as plt
import re,json,jieba,pandas
from collections import Counter
# from wordcloud import WordCloud
# import seaborn as sns
from scipy.interpolate import spline
# matprotlib显示中文
from pylab import *
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# 从mysql中获取数据
def data_analysis():
    cursor, conn = connect_mysql()
    class_sql='SELECT class FROM food_rank'
    cursor.execute(class_sql)
    class_all=set(list(cursor.fetchall()))
    shop_list_all=[]
    # for each in class_all[:]:
    #     class_all.append(each[0])
    #     class_all.remove(each)
    for each in class_all:
        shop_sql='SELECT shopName,mainRegionName,taste,environment,service,avgPrice FROM food_rank WHERE class="{}";'.format(each[0])
        # print(shop_sql)
        cursor.execute(shop_sql)
        shop_list=cursor.fetchall()
        shop_list_all.append(shop_list)
    # print(shop_list_all)
    cursor.close()
    conn.close()
    return shop_list_all

# data_analysis()
def get_shop_list():
    shop_list_all=data_analysis()
    shopNames = []
    tastes = []
    environments=[]
    services = []
    avgPrices = []
    for shop_list in shop_list_all[:1]:
        for shop in shop_list[:21]:
            shopNames.append(shop[0])
            tastes.append(shop[2])
            environments.append(shop[3])
            services.append(shop[4])
            avgPrices.append(int(shop[5])*0.01)
        shopNames=pandas.DataFrame({'shopNames':shopNames})
        tastes = pandas.DataFrame({'tastes': tastes})
        services = pandas.DataFrame({'services': services})
        environments=pandas.DataFrame({'environments':environments})
        avgPrices = pandas.DataFrame({'avgPrices': avgPrices})
        data = pandas.concat([shopNames, tastes,environments,services,avgPrices], axis=1, ignore_index=True)
        data.columns = ['shopNames', 'tastes','environments','services','avgPrices']
        # print(data)
        plot_graph(data.shopNames,data.tastes,data.environments,data.services,data.avgPrices)
# get_shop_list()

def plot_graph(shopNames, tastes,environments,services,avgPrices):
    # 开始画图
    # sub_axix = shopNames
    plt.style.use('dark_background')
    plt.title('分析')
    plt.figure(figsize=(35, 15))
    plt.xticks(rotation=60)
    plt.plot(shopNames, tastes, color='green', label='口味',)
    plt.plot(shopNames, environments, color='skyblue', label='环境')
    plt.plot(shopNames, services, color='red', label='服务')
    # plt.plot(shopNames, avgPrices, color='skyblue', label='avgPrices')
    # plt.plot(shopNames, thresholds, color='blue', label='threshold')
    plt.legend() # 显示图例
    plt.xlabel('商铺')
    plt.ylabel('评分')
    plt.show() #python 一个折线图绘制多个曲线

get_shop_list()

