# -*- coding: utf-8 -*-
# @Time    : 2023/7/23 15:56
# @Author  : chenyinhua
# @File    : test_login.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import scenarios
# 本地应用/模块导入
from pages.login_page import *
from pages.common_page import *

scenarios('./login.feature')
