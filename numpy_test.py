#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-19 13:46
# @file : numpy_test.py
# @software : PyCharm

import numpy as np

# a=np.arange(24)
# print(a.ndim)
# print(a.shape)
# print(a.itemsize)

# a = np.arange(0,60,5)
# for x in np.nditer(a):
#     print(x)

# a = np.arange(0,60,5)
# a = a.reshape(3,4)
# b = a.T
# c = b.copy(order='C')   #以 C 风格顺序排序
# for x in np.nditer(c):
#     print(x)
# c = b.copy(order='F')   #以 F 风格顺序排序
# for x in np.nditer(c):
#     print(x)
import pandas as pd
# 查看每一列的数据类型

# names = ['Bob','Jessica','Mary','John','Mel','John','Mel']
# births = [968, 155, 77, 578, 973, 578, 973]
# data=list(zip(names,births))
# df=pd.DataFrame(data=data,columns=['names','births'])
# # 查看每一列的数据类型
# print df.dtypes
# # 查看指定列的数据类型
# print df

# d = {'one':[1,1,1,1,1],
#      'two':[2,2,2,2,2],
#      'letter':['a','a','b','b','c']}
#
# # 创建一个 dataframe
# df = pd.DataFrame(d)
# print df
#
# one=df.groupby('letter')
# two=df.groupby(['letter','one']).sum()
# # 不把用来分组的列名作为索引
# three=df.groupby(['letter','one'],as_index=False).sum()
# print one.sum()
# print two
# # 输出索引
# print two.index
# print three.index


# 创建一个 dataframe，用日期作为索引
# States = ['NY', 'NY', 'NY', 'NY', 'FL', 'FL', 'GA', 'GA', 'FL', 'FL']
# # data = [1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # idx = pd.date_range('1/1/2012', periods=10, freq='MS')
# # df1 = pd.DataFrame(data, index=idx, columns=['Revenue'])
# # df1['State'] = States
# #
# # # 创建第二个 dataframe
# # data2 = [10.0, 10.0, 9, 9, 8, 8, 7, 7, 6, 6]
# # idx2 = pd.date_range('1/1/2013', periods=10, freq='MS')
# # df2 = pd.DataFrame(data2, index=idx2, columns=['Revenue'])
# # df2['State'] = States
# #
# # # 把两个 dataframe 合并起来
# # df = pd.concat([df1,df2])
# # print df

from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://root:zkyr1006@localhost:3306/mydb')



















