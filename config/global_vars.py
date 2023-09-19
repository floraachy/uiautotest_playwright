# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/31 14:31
# @Author  : chenyinhua
# @File    : global_vars.py
# @Software: PyCharm
# @Desc: 全局变量

# 定义一个全局变量，用于存储运行过程中相关数据
GLOBAL_VARS = {}


ENV_VARS = {
    "common": {
        "报告标题": "UI自动化测试报告",
        "项目名称": "GitLink 确实开源",
        "测试人": "陈银花",
        "所属部门": "开源中心"
    },
    "test": {
        # 示例测试环境及示例测试账号
        "host": "https://testforgeplus.trustie.net",
        "login": "auotest",
        "password": "12345678",
        "nickname": "AutoTest",
        "user_id": "84954",
        "project_id": "",
        "project": ""

    },
    "live": {
        "host": "https://www.gitlink.org.cn",
        "login": "",
        "password": "",
        "nickname": "******",
        "user_id": "******",
        "project_id": "",
        "project": ""
    }
}
