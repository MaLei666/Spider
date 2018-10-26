#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-24 10:37
# @file : app_test.py
# @software : PyCharm

import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'  #设备系统
desired_caps['platformVersion'] = '8.0.0'  #设备系统版本
desired_caps['deviceName'] = 'Galaxy S8'  #设备名称
# desired_caps['app'] = PATH('D:\\下载\\jumeilatest.apk')
desired_caps['appPackage'] = 'com.jm.android.jumei'
desired_caps['appActivity'] = 'com.jm.android.jumei.home.activity.StartActivity'


driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(6)
x=driver.get_window_size()['width']
y=driver.get_window_size()['height']# 左滑
driver.swipe(x*0.75,y*0.5,x*0.25,y*0.5,100)
time.sleep(2)
# 上滑
driver.swipe(x*0.5,y*0.75,x*0.5,y*0.2,100)
print('手动点击登录')
time.sleep(6)
print('使用微信登录')
driver.tap([(159,1890),(349,1986)],100)
# 手动关掉弹窗
time.sleep(2)
# driver.launch_app()
for i in range(0,10):
    time.sleep(17)
    driver.swipe(x*0.5,y*0.75,x*0.5,y*0.25,200)

# 收起键盘
driver.hide_keyboard()
# 查看当前activity，只适用于Android
driver.current_activity()
# 设备中拉出文件
driver.pull_file('/path')
# 推送文件
data='test'
driver.push_file('/path',data.encode('base64'))
driver.shake()