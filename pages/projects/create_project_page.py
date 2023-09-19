# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:10
# @Author  : chenyinhua
# @File    : create_project_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import random
# 第三方库导入
from pytest_bdd import when, then
from playwright.sync_api import Page
from loguru import logger
# 本地应用/模块导入
from case_utils.allure_handle import allure_step
from case_utils.data_handle import data_handle, eval_data_process
from config.global_vars import GLOBAL_VARS

case = {
    "name": "Auto Test ${generate_name()}",
    "identifier": "${generate_identifier()}",
    "desc": "${generate_name()}",
    "category": random.choice(["机器学习", "大数据", "深度学习", "人工智能", "量子计算", "智慧医疗", "自动驾驶", "其他"]),
    "language": random.choice(["C#", "HTML", "CSS", "Python3.6"]),
    "gitignore": random.choice(["Ada", "Actionscript", "Ansible", "Android", "Agda"]),
    "license": random.choice(["0BSD", "AAL", "AFL-1.1", "389-exception"]),
}
case = eval_data_process(data_handle(obj=case, source=None))

logger.debug(f"打印用例，定位一下：{case}")


@when(name="输入项目名称：<name>， 项目标识：<identifier>, 项目简介：<desc>")
def input_name_identifier_desc(page: Page, name=case["name"], identifier=case["identifier"], desc=case["desc"]):
    # 输入项目名称
    page.fill(selector="xpath=//input[@id='NewWorkForm_name']", value=name)
    allure_step(step_title=f"输入项目名称：{name}")
    # 输入项目标识
    page.fill(selector="xpath=//input[@id='NewWorkForm_repository_name']", value=identifier)
    allure_step(step_title=f"输入项目标识：{identifier}")
    # 输入项目简介
    page.fill(selector="xpath=//textarea[@id='NewWorkForm_description']", value=desc)
    allure_step(step_title=f"输入项目名称：{desc}")


@when(name="选择.gitignore: <gitignore>，开源许可证: <licence>，项目类别: <type>，项目语言: <language>")
def choose_gitignore_licence_language_type(page: Page, gitignore=case["gitignore"], license=case["license"],
                                           language=case["language"], category=case["category"]):
    # 选择gitignore
    page.click(selector="xpath=//input[@id='NewWorkForm_ignoreFlag']")
    page.click(selector="xpath=//div[@id='NewWorkForm_ignore']")
    page.click(selector=f"//li[text()='{gitignore}']")
    allure_step(step_title=f"选择gitignore：{gitignore}")

    # 选择开源许可证
    page.click(selector="xpath=//input[@id='NewWorkForm_licenseFlag']")
    page.click(selector="xpath=//div[contains(text(), '请选择开源许可证')]")
    page.click(selector=f"//li[text()='{license}']")
    allure_step(step_title=f"选择开源许可证：{license}")
    # 选择项目类别
    page.click(selector="xpath=//input[@id='NewWorkForm_categoreFlag']")
    page.click(selector="xpath=//div[text()='请选择项目类别']")
    page.click(selector=f"//li[text()='{category}']")
    allure_step(step_title=f"选择项目类别：{category}")

    # 往下滑动
    js = "window.scrollTo(0, 200)"
    page.evaluate(js)

    # 选择项目语言
    page.click(selector="xpath=//input[@id='NewWorkForm_languageFlag']")
    page.click(selector="xpath=//div[text()='请选择项目语言']")
    page.click(selector=f"//li[text()='{language}']")
    allure_step(step_title=f"选择项目语言：{language}")


@when("勾选复选框，将项目设为私有")
def check_private_checkbox(page: Page):
    # 通过id定位使用#   通过css定位使用.
    page.check(selector="#NewWorkForm_private")
    allure_step(step_title=f"勾选复选框，将项目设为私有")


@when(name="点击：创建项目 按钮，提交新建项目表单")
def submit_project_button(page: Page):
    page.click(selector="xpath=//span[text()='创建项目']/parent::button")
    allure_step(step_title="点击创建项目按钮，提交新建项目表单")
    page.wait_for_timeout(10000)  # 超时时间是10s


@then("当前页面的url地址应该是：<host>/<project_url>")
def check_current_url(page: Page, host, project_url=f'{GLOBAL_VARS["login"]}/{case["identifier"]}'):
    expected = f"{host}/{project_url}"
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    assert expected == actual
