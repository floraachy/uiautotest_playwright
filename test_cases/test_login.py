# -*- coding: utf-8 -*-
# @Time    : 2023/7/23 15:56
# @Author  : chenyinhua
# @File    : test_login.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import scenarios, given, when, then, parsers
from sttable import parse_str_table
from playwright.sync_api import Page, expect
# 本地应用/模块导入
from case_utils.allure_handle import allure_step

scenarios('./login.feature')


@given("打开浏览器，访问项目首页<host>/explore")
def visit_projects_home(page: Page, host):
    page.goto(host + "/explore")


@given("打开浏览器，访问GitLink首页<host>")
def visit_home(page: Page, host):
    page.goto(host)


@when("点击:登录按钮，进入登录页面")
@when("点击:登录按钮，打开登录弹窗")
def click_login_button(page: Page):
    page.click(selector="xpath=//a[text()='登录']")


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
        allure_step(step_title=f"登录弹窗输入--> 用户名: {login}  密码：{password}")


@when(parsers.parse("登录页面中，我输入以下信息进行登录：\n{user_info}"))
def input_login_info(page: Page, user_info):
    users = parse_str_table(user_info)
    for row in users.rows:
        login = row["用户名"]
        password = row["密码"]
        page.fill(selector="id=login_username", value=login)
        page.fill(selector="id=login_password", value=password)
        allure_step(step_title=f"登录弹窗输入--> 用户名: {login}  密码：{password}")
        allure_step(step_title=f"登录页面输入--> 用户名: {login}  密码：{password}")


@when("弹窗中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_pop(page: Page):
    page.click(selector="xpath=//div[text()='登录']")
    allure_step(step_title=f"登录弹窗中，点击登录按钮，提交登录表单")


@when("登录页面中，点击: 登录按钮， 提交登录表单")
def submit_login_button_on_page(page: Page):
    page.click(selector="xpath=//span[text()='登 录']/..")
    allure_step(step_title=f"登录页面中，点击登录按钮，提交登录表单")
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


@then(parsers.parse("登录成功，右上角显示的用户昵称应该是：{login}"))
def check_username(page: Page, login):
    login_element = page.locator(selector="xpath=//a[@class='ant-dropdown-trigger']")
    actual = login_element.get_attribute("href")
    expected = f"/{login}"
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual


@then(parsers.parse("登录失败，页面有密码错误提示：{expected_error}"))
def check_login_error(page: Page, expected_error):
    expected = expected_error
    error_element = page.query_selector(selector="xpath=//p[contains(@class, 'message')]")
    actual = error_element.text_content()
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual
