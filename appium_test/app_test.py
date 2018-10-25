#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2018-10-24 10:37
# @file : app_test.py
# @software : PyCharm

import os
import time
import unittest
from selenium import webdriver
from lib2to3.pgen2.driver import Driver
# from lib2to3.tests.support import driver
from appium import webdriver

PATH=lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))

desired_caps = {}
desired_caps['platformName'] = 'Android'  #设备系统
desired_caps['platformVersion'] = '8.0.0'  #设备系统版本
desired_caps['deviceName'] = 'Galaxy S8'  #设备名称
# desired_caps['app'] = PATH('D:\\下载\\jumeilatest.apk')
desired_caps['appPackage'] = 'com.jm.android.jumei'
desired_caps['appActivity'] = 'com.jm.android.jumei.home.activity.StartActivity'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# driver.launch_app()
time.sleep(10)

