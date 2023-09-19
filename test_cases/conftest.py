# -*- coding: utf-8 -*-
# @Time    : 2023/3/17 18:33
# @Author  : Flora.Chen
# @File    : conftest.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
import pytest
import requests
from loguru import logger
from pytest_bdd import given
from playwright.sync_api import Page
# 本地应用/模块导入
from config.global_vars import GLOBAL_VARS
from common_utils.base_request import BaseRequest


@pytest.fixture(scope="session")
def host():
    return GLOBAL_VARS.get("host")


@given(name="写入登录cookies，并刷新页面")
def write_login_cookies(page: Page, login_api, host):
    cookies_dict = login_api[0]
    cookies_list = [{'name': name, 'value': value, 'url': host} for name, value in cookies_dict.items()]
    page.context.add_cookies(cookies_list)
    page.reload()


@pytest.fixture(scope="module")
def login_api():
    """
    获取登录的cookie
    :return:
    """
    host = GLOBAL_VARS.get("host")
    login = GLOBAL_VARS.get('login')
    password = GLOBAL_VARS.get('password')
    # 兼容一下host后面多一个斜线的情况
    if host[-1] == "/":
        host = host[:len(host) - 1]
    req_data = {
        "url": host + "/api/accounts/login.json",
        "method": "POST",
        "request_type": "json",
        "headers": {"Content-Type": "application/json; charset=utf-8;"},
        "payload": {"login": login, "password": password, "autologin": 1}
    }
    # 请求登录接口
    try:
        res = BaseRequest.send_request(req_data=req_data)
        res.raise_for_status()
        # 将cookies转成字典
        cookies = requests.utils.dict_from_cookiejar(res.cookies)
        logger.debug(f"获取用户：{login}登录的cookies成功：{type(cookies)} || {cookies}")
        yield cookies, res.json()
    except Exception as e:
        GLOBAL_VARS["login_cookie"] = None
        logger.error(f"获取用户：{login}登录的cookies失败：{e}")
