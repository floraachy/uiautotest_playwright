# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:07
# @Author  : chenyinhua
# @File    : common_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page, expect
# 本地应用/模块导入
from case_utils.allure_handle import allure_step
from config.global_vars import GLOBAL_VARS


@given("打开浏览器，访问项目首页<host>/explore")
def visit_projects_home(page: Page, host):
    page.goto(host + "/explore")


@given("打开浏览器，访问GitLink首页<host>")
def visit_home(page: Page, host):
    page.goto(host)


@then("当前页面跳转到用户个人主页：<host>/<login>")
def check_current_url_on_page(page: Page, host, login=GLOBAL_VARS.get("login")):
    expected = f'{host}/{login}'
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    expect(page).to_have_url(expected)


@when(name="点击导航栏右上角的新建图标")
def click_new_icon(page: Page):
    page.hover(selector="xpath=//i[contains(@class, 'icon-sousuo')]/following-sibling::img")


@then(name="点击新建图标下的新建项目按钮，进入新建项目页面")
def click_new_project_button(page: Page):
    page.click(selector="xpath=//a[text()='新建项目']")


@when("点击导航栏右上角的登录按钮，进入登录页面")
@when("点击导航栏右上角的登录按钮，打开登录弹窗")
def click_login_button(page: Page):
    page.click(selector="xpath=//a[text()='登录']")


@then(parsers.parse("登录成功，导航栏右上角显示的用户昵称应该是：{login}"))
def check_username(page: Page, login):
    login_element = page.locator(selector="xpath=//a[@class='ant-dropdown-trigger']")
    actual = login_element.get_attribute("href")
    expected = f"/{login}"
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual
