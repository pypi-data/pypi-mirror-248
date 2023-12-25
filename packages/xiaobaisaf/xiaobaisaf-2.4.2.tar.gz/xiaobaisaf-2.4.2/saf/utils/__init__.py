#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/20 23:04
@File  : __init__.py.py
'''
'''
    工具类或者工具函数
    1、文件解析
    2、数据加密等操作
'''
import glob, sys, os, platform

SELENIUM_MANAGER_FULL_PATH = \
    glob.glob(fr'{os.path.dirname(sys.executable)}/**/selenium/webdriver/common/{"macos" if platform.system() == "Darwin" else platform.system().lower()}/selenium-manager**',
    recursive=True)[0]
