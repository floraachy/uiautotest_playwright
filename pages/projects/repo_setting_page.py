# -*- coding: utf-8 -*-
# @Time    : 2023/9/19 15:13
# @Author  : chenyinhua
# @File    : repo_setting_page.py
# @Software: PyCharm
# @Desc:

# 标准库导入
# 第三方库导入
from pytest_bdd import when, then
from playwright.sync_api import Page, expect
# 本地应用/模块导入


@when("滚动到底部，点击 删除本仓库 按钮")
def click_delete_repo_button(page: Page):
    # 往下滑动
    js = "window.scrollTo(0, document.documentElement.scrollHeight)"
    page.evaluate(js)
    page.click("xpath=//span[text()='删除本仓库']")


@when('在弹出确认提示弹窗"该操作无法撤销！且将会一并删除相关的疑修、合并请求、工作流、里程碑、动态等数据" 中 点击 确定 按钮')
def click_delete_repo_confirm_button(page: Page):
    locator = page.locator("xpath=//span[contains(text(), '该操作无法撤销')]")
    expect(locator).to_be_visible()
    page.click("xpath=//a[text()='确定']")


@then('仓库删除成功，有成功提示"仓库删除成功！"')
def check_delete_success_text(page: Page):
    locator = page.locator("xpath=//div[text()='仓库删除成功！']")
    expect(locator).to_contain_text("仓库删除成功！")
