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

import numpy as np
a = np.array([0,30,45,60,90])
print  '不同角度的正弦值：'
# 通过乘 pi/180 转化为弧度
print np.sin(a*np.pi/180)
print  '\n'
print  '数组中角度的余弦值：'
print np.cos(a*np.pi/180)
print  '\n'
print  '数组中角度的正切值：'
print np.tan(a*np.pi/180)