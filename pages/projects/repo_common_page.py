# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:16
# @Author  : chenyinhua
# @File    : repo_common_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import when, then
from playwright.sync_api import Page, expect
# 本地应用/模块导入
from case_utils.allure_handle import allure_step


@then("当前应该不存在 私有 标签")
def check_private_tag(page: Page):
    locator = page.locator("xpath=//span[text()='私有']")
    expect(locator, "当前应该不存在 私有 标签").to_be_hidden()


@then("当前应该 存在 私有 标签")
def check_private_tag_exist(page: Page):
    locator = page.locator("xpath=//span[text()='私有']")
    expect(locator, "当前应该不存在 私有 标签").to_be_visible()


@when("点击 仓库设置 导航栏，进入仓库基本设置页面")
def click_repo_setting_button(page: Page):
    page.click("xpath=//span[text()='仓库设置']")
    allure_step(step_title="点击 仓库设置按钮")
