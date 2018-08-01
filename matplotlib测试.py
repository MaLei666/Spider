# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt

# 方程图
# x=np.arange(1,11)
# y=2*x+5
# plt.title('方程')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.plot(x,y)
# plt.show()

# sin和cos图
# x=np.arange(0,3*np.pi,0.1)
# y_sin=np.sin(x)
# y_cos=np.cos(x)
# plt.subplot(2,1,1)
# plt.plot(x,y_sin)
# plt.title('sin')
# plt.subplot(2,1,2)
# plt.plot(x,y_cos)
# plt.title('cos')
# plt.show()

# 条形图
# plt.bar([1,3,5,7,9], [5,3,7,8,3],label='first')
# plt.bar([2,4,6,8,10], [12,3,2,6,4],color='g',label='second')
# plt.title('bar')
# plt.legend()
# plt.ylabel('y')
# plt.xlabel('x')
# plt.show()

# 直方图
# a=np.array([22,87,5,43,56,73,55,54,11,20,51,5,79,31,27])
# plt.hist(a,bins=[0,20,40,60,80,100],color='g',histtype='bar', rwidth=0.8)
# plt.title('histogrm')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.legend()
# plt.show()

# # 散点图
# x = [1,2,3,4,5,6,7,8]
# y = [5,2,4,2,1,4,5,2]   #如果在 3 维绘制则是 3 个。
# plt.scatter(x,y, label='skits', color='k', s=25, marker="o")
# plt.legend()
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.show()

# 堆叠图
# days = [1,2,3,4,5]
# sleeping = [7,8,6,11,7]
# eating =   [2,3,4,3,2]
# working =  [7,8,7,2,2]
# playing =  [8,5,7,8,13]
# # 画一些空行，给予它们符合我们的堆叠图的相同颜色
# plt.plot([],[],color='m', label='Sleeping', linewidth=5)
# plt.plot([],[],color='c', label='Eating', linewidth=5)
# plt.plot([],[],color='r', label='Working', linewidth=5)
# plt.plot([],[],color='k', label='Playing', linewidth=5)
# plt.stackplot(days,sleeping,eating,working,playing, colors=['m','c','r','k'])
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()

# 饼图
# slices = [7,2,2,13]
# activities = ['sleeping','eating','working','playing']
# cols = ['c','m','r','b']
# plt.pie(slices,         # 切片
#         labels=activities,  #
#         colors=cols,    # 颜色列表
#         startangle=90,  # 指定图形的起始角度
#         shadow= True,   # 给绘图添加一个字符大小的阴影
#         explode=(0,0.1,0,0),    # 拉出第二个切片
#         autopct='%1.1f%%')  # 百分比放置到图表上
# plt.title('Interesting Graph\nCheck it out')
# plt.show()

# 加载数据
# # 将索引为0的元素存储到x列表，将索引为1的元素存储到y列表中
# x, y = np.loadtxt('E:\Spider\output.txt', delimiter=',', unpack=True)
# plt.plot(x,y, label='Loaded from file!')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Interesting Graph\nCheck it out')
# plt.legend()
# plt.show()

from mpl_toolkits.basemap import Basemap
# basemap地理绘图
# m = Basemap(projection='mill',
#             llcrnrlat = -90,    # 左下角的纬度
#             llcrnrlon = -180,   # 左下角的经度
#             urcrnrlat = 90,     # 右上角的纬度
#             urcrnrlon = 180,    # 右上角的经度
#             resolution='l')  #分辨率 c:粗糙，l：低，h：高，f：完整
# m.drawcoastlines()
# m.drawcountries(linewidth=2)  # 画出国家，线宽为2
# ##m.drawstates(color='b')  #蓝色线条画出州
# ##m.drawcounties(color='darkred')  #画出国家，黑色
# m.etopo()  #模型版本
# # m.bluemarble()  #模型版本
# plt.title('Basemap Tutorial')
# plt.show()

# 绘制坐标
# m = Basemap(projection='mill',
#             llcrnrlat = 10,
#             llcrnrlon = 73,
#             urcrnrlat = 54,
#             urcrnrlon = 135,
#             resolution='l')
# m.drawcoastlines()
# m.drawcountries(linewidth=2)
# m.etopo()
#
# xs = []
# ys = []
# beij1, beij2 = 116.405913, 39.916237
# xpt, ypt = m(beij1, beij2)
# xs.append(xpt)
# ys.append(ypt)
# m.plot(xpt, ypt, 'r*', markersize=15)
#
# sh1, sh2 = 121.475941, 31.235435
# xpt, ypt = m(sh1, sh2)
# xs.append(xpt)
# ys.append(ypt)
# m.plot(xpt, ypt, 'r*', markersize=15)
#
# xj1, xj2 = 87.60243,43.827547
# xpt, ypt = m(xj1, xj2)
# xs.append(xpt)
# ys.append(ypt)
# m.plot(xpt, ypt, 'r*', markersize=15)
# m.plot(xs, ys, color='k', linewidth=3, label='Flight 98')  # 直线连接
# m.drawgreatcircle(beij1, beij2, xj1, xj2, color='r', linewidth=3, label='Arc') # 弧线连接
# plt.legend(loc=4)
# plt.title('Basemap Tutorial')
# plt.show()

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use('ggplot')

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

x3 = [1,2,3,4,5,6,7,8,9,10]
y3 = [5,6,7,8,2,5,6,3,7,2]
z3 = np.zeros(10)

dx = np.ones(10)
dy = np.ones(10)
dz = [1,2,3,4,5,6,7,8,9,10]

ax1.bar3d(x3, y3, z3, dx, dy, dz)


ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')

plt.show()

