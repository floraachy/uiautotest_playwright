# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:10
# @Author  : chenyinhua
# @File    : create_project_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import when, then, parsers
from playwright.sync_api import Page
# 本地应用/模块导入
from case_utils.allure_handle import allure_step
from config.global_vars import GLOBAL_VARS


@when(parsers.parse("输入项目名称: {name}, 项目标识: {identifier}, 项目简介: {desc}"))
def input_name_identifier_desc(page: Page, name, identifier, desc):
    # 输入项目名称
    page.fill(selector="xpath=//input[@id='NewWorkForm_name']", value=name)
    # 输入项目标识
    page.fill(selector="xpath=//input[@id='NewWorkForm_repository_name']", value=identifier)
    GLOBAL_VARS["identifier"] = identifier
    # 输入项目简介
    page.fill(selector="xpath=//textarea[@id='NewWorkForm_description']", value=desc)


@when(parsers.parse("选择.gitignore: {gitignore}，开源许可证: {certificate}"))
def choose_gitignore_licence(page: Page, gitignore, certificate):
    # 选择gitignore
    page.click(selector="xpath=//input[@id='NewWorkForm_ignoreFlag']")
    page.click(selector="xpath=//div[@id='NewWorkForm_ignore']")
    page.click(selector=f"//li[text()='{gitignore}']")

    # 选择开源许可证
    page.click(selector="xpath=//input[@id='NewWorkForm_licenseFlag']")
    page.click(selector="xpath=//div[contains(text(), '请选择开源许可证')]")
    page.click(selector=f"//li[text()='{certificate}']")


@when(parsers.parse("选择项目类别: {category}，项目语言: {language}"))
def choose_category_language(page: Page, category, language):
    page.click(selector="xpath=//input[@id='NewWorkForm_categoreFlag']")
    page.click(selector="xpath=//div[text()='请选择项目类别']")
    page.click(selector=f"//li[text()='{category}']")

    # 往下滑动
    js = "window.scrollTo(0, 200)"
    page.evaluate(js)

    page.click(selector="xpath=//input[@id='NewWorkForm_languageFlag']")
    page.click(selector="xpath=//div[text()='请选择项目语言']")
    page.click(selector=f"//li[text()='{language}']")


@when("勾选复选框，将项目设为私有")
def check_private_checkbox(page: Page):
    # 通过id定位使用#   通过css定位使用.
    page.check(selector="#NewWorkForm_private")


@when(name="点击：创建项目 按钮，提交新建项目表单")
def submit_project_button(page: Page):
    page.click(selector="xpath=//span[text()='创建项目']/parent::button")
    page.wait_for_timeout(10000)  # 超时时间是10s


@then("当前页面的url地址应该是：<host>/<project_url>")
def check_current_url(page: Page, host):
    expected = f"{host}/{GLOBAL_VARS['login']}/{GLOBAL_VARS['identifier']}"
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual
