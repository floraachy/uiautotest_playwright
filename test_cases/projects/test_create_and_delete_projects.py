# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:26
# @Author  : chenyinhua
# @File    : test_create_and_delete_projects.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import random
# 第三方库导入
from pytest_bdd import scenarios, given, when, then
from playwright.sync_api import Page, expect
from loguru import logger
# 本地应用/模块导入
from case_utils.allure_handle import allure_step
from case_utils.data_handle import data_handle, eval_data_process
from config.global_vars import GLOBAL_VARS

scenarios('./projects/create_and_delete_projects.feature')

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


@given("打开浏览器，访问GitLink首页<host>")
def visit_home(page: Page, host):
    page.goto(host)


@when(name="点击导航栏右上角的新建图标")
def click_new_icon(page: Page):
    page.hover(selector="xpath=//i[contains(@class, 'icon-sousuo')]/following-sibling::img")
    allure_step(step_title=f"登录状态下，点击右上角 新建 图标，显示：新建项目，导入项目，新建组织，加入项目")


@then(name="点击新建图标下的新建项目按钮，进入新建项目页面")
def click_new_project_button(page: Page):
    page.click(selector="xpath=//a[text()='新建项目']")
    allure_step(step_title=f"登录状态下，点击右上角 新建>新建项目 按钮")


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
    allure_step('当前弹出确认提示弹窗"该操作无法撤销！且将会一并删除相关的疑修、合并请求、工作流、里程碑、动态等数据"')
    page.click("xpath=//a[text()='确定']")
    allure_step('当前弹出确认提示弹窗中 点击 确定 按钮')


@then('仓库删除成功，有成功提示"仓库删除成功！"')
def check_delete_success_text(page: Page):
    locator = page.locator("xpath=//div[text()='仓库删除成功！']")
    expect(locator).to_contain_text("仓库删除成功！")


@then("当前页面跳转到用户个人主页：<host>/<login>")
def check_current_url_on_page(page: Page, host, login=GLOBAL_VARS.get("login")):
    expected = f'{host}/{login}'
    actual = page.url
    allure_step(step_title=f"预期结果：{expected} || 实际结果：{actual}")
    expect(page).to_have_url(expected)
