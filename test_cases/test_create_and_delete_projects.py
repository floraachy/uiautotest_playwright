# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:26
# @Author  : chenyinhua
# @File    : test_create_and_delete_projects.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import scenarios
# 本地应用/模块导入
from pages.common_page import *
from pages.projects.create_project_page import *
from pages.projects.repo_common_page import *
from pages.projects.repo_setting_page import *


scenarios('./projects/create_and_delete_projects.feature')




