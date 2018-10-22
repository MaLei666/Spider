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


d1 = {'one':[1,1],
     'two':[2,2],
     'letter':['a','b']}
d2 = {'one':[1,1],
     'two':[2,2],
     'letter':['a','b']}
d1=pd.DataFrame(d1,columns=['d1'])
d2=pd.DataFrame(d2,columns=['d2'])
df=pd.concat([d1,d2])
print df