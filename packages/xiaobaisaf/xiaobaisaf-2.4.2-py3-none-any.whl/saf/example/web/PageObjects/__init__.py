#! /usr/bin/env python
# -*- coding=utf-8 -*-
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:05
@File  : __init__.py
'''

#********************************#
#\t欢迎使用自动生成POM代码工具\t#
#\tAuther : xiaobaiTser\t\t#
#********************************#

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

Options = webdriver.ChromeOptions()
# Options.add_experimental_option('useAutomationExtension', False)      # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
# Options.add_experimental_option('excludeSwitches', ['--enable-automation'])  # 去除"Chrome正在受到自动化测试软件的控制"弹出框信息
# Options.add_experimental_option('detach', True)                       # 禁止自动关闭浏览器
# Options.add_argument('--blink-settings=imagesEnabled=false')          # 隐藏图片
# Options.add_argument('--no-sandbox')
# Options.add_argument('--disable-dev-shm-usage')
# Options.add_argument('--headless')                                    # 隐藏浏览器界面
# Options.add_argument('--disable-gpu')
# Options.add_argument('--ignore-certificate-errors')
# Options.add_argument('--ignore-ssl-errors')
# Options.add_argument('--disable-extensions')
# Options.add_argument('--disable-blink-features=AutomationControlled') # 隐藏Webdriver特征
driver = webdriver.Chrome(options=Options)