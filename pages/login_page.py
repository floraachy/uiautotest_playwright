# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:06
# @Author  : chenyinhua
# @File    : login_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import when, then, parsers
from sttable import parse_str_table
from playwright.sync_api import Page, expect
# 本地应用/模块导入
from case_utils.allure_handle import allure_step


@when(parsers.parse("弹窗中，我输入以下信息进行登录：\n{user_info}"))
def input_login_info_on_pop(page: Page, user_info):
    # 通过sttable.parse_str_table获取测试步骤中表格的内容
    # 获取到的格式是这样的：[{'用户名': 'xxxxxx', '密码': 'xxxxxx'}]
    users = parse_str_table(user_info)
    for row in users.rows:
        login = row["用户名"]
        password = row["密码"]
        page.fill(selector="xpath=//input[@name='username']", value=login)
        page.fill(selector="xpath=//input[@name='password']", value=password)


@when(parsers.parse("登录页面中，我输入以下信息进行登录：\n{user_info}"))
def input_login_info(page: Page, user_info):
    users = parse_str_table(user_info)
    for row in users.rows:
        login = row["用户名"]
        password = row["密码"]
        page.fill(selector="id=login_username", value=login)
        page.fill(selector="id=login_password", value=password)


@when("弹窗中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_pop(page: Page):
    page.click(selector="xpath=//div[text()='登录']")


@when("登录页面中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_page(page: Page):
    page.click(selector="xpath=//span[text()='登 录']/..")
    # page.wait_for_timeout(10000)  # 超时时间是10s
    page.wait_for_load_state()


@then("当前页面的url地址应该是：<host>/explore")
def check_current_url_on_pop(page: Page, host):
    expected = f'{host}/explore'
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    expect(page).to_have_url(expected)


@then(parsers.parse("登录成功，当前页面的url地址应该是：<host>/{login}"))
def check_current_url_on_page(page: Page, host, login):
    expected = f'{host}/{login}'
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    expect(page).to_have_url(expected)


@then(parsers.parse("登录失败，页面有密码错误提示：{expected_error}"))
def check_login_error(page: Page, expected_error):
    expected = expected_error
    error_element = page.query_selector(selector="xpath=//p[contains(@class, 'message')]")
    actual = error_element.text_content()
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual
