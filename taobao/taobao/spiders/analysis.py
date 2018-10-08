#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-06 12:50
# @file : analysis.py
# @software : PyCharm
import numpy
from pymongo import MongoClient
from  matplotlib import pyplot as plt

def data_analysis():
    sell_count = []
    client=MongoClient('mongodb://admin:zkyr1006@localhost:28018')
    db=client.taobao
    collection=db.内搭
    result=collection.find({'price'})

def plot():
    plt.figure(figsize=(8,4))
    data
