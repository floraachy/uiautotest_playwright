# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 17:27
# @Author  : chenyinhua
# @File    : path_config.py
# @Software: PyCharm
# @Desc: 项目相关路径

# 标准库导入
import os

# ------------------------------------ 项目路径 ----------------------------------------------------#
# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 通用模块目录
COMMON_DIR = os.path.join(BASE_DIR, "common_utils")

# 配置模块目录
CONF_DIR = os.path.join(BASE_DIR, "config")

# 日志/报告保存目录
OUT_DIR = os.path.join(BASE_DIR, "outputs")
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

# 报告保存目录
REPORT_DIR = os.path.join(OUT_DIR, "report")
if not os.path.exists(REPORT_DIR):
    os.mkdir(REPORT_DIR)

# 日志保存目录
LOG_DIR = os.path.join(OUT_DIR, "log")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 图片保存的目录
IMG_DIR = os.path.join(OUT_DIR, "image")
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

# 第三方库目录
LIB_DIR = os.path.join(BASE_DIR, "lib")

# Allure报告，测试结果集目录
ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, "allure_results")

# Allure报告，HTML测试报告目录
ALLURE_HTML_DIR = os.path.join(REPORT_DIR, "allure_html")
