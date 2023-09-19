# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/2/2 16:05
# @Author  : chenyinhua
# @File    : conftest.py
# @Software: PyCharm
# @Desc: 这是文件的描述信息

# 标准库导入
import time
import os
from datetime import datetime
# 第三方库导入
from loguru import logger
import pytest
# 本地应用/模块导入
from config.path_config import IMG_DIR
from case_utils.allure_handle import allure_step, allure_title
from config.settings import RunConfig


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": RunConfig.window_size
    }


# ------------------------------------- START: pytest-bdd钩子函数处理---------------------------------------#
def pytest_bdd_apply_tag(tag, function):
    """
    自定义标记转换为 pytest 标记的行为
    """
    if tag == 'todo':
        marker = pytest.mark.skip(reason="还没有处理完成~")
        marker(function)
        return True
    else:
        return None


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """
    当步骤函数执行失败时调用。可以在此处理步骤失败的情况。它接收 request 对象、feature 对象、scenario 对象、step 对象、step_func 函数、step_func_args 参数和 exception 异常对象作为参数。
    :param request: 包含有关测试请求的信息。
    :param feature: 当前特性的元数据。
    :param scenario: 当前场景的元数据。
    :param step: 当前步骤的元数据。
    :param step_func: 当前步骤的函数对象。
    :param step_func_args: 当前步骤的函数参数。
    :param exception: 捕获到的异常对象。
    :return:
    """

    feature_name = getattr(feature, 'name', None)
    feature_description = getattr(feature, 'description', None)

    scenario_name = getattr(scenario, 'name', None)

    step_name = getattr(step, "name", None)

    logger.error("\n" + "=" * 80
                 + "\n-------------测试步骤出错了--------------------\n"
                   f"Feature: {feature_name}\n"
                   f"Scenario: {scenario_name}\n"
                   f"Step: {step}\n"
                   f"Exception:   {exception}\n"
                 + "=" * 80)
    print("\n" + "=" * 80
          + "\n-------------测试步骤出错了--------------------\n"
            f"Feature: {feature_name}\n"
            f"Scenario: {scenario_name}\n"
            f"Step: {step}\n"
            f"Exception:   {exception}\n"
          + "=" * 80)

    allure_step(step_title=f"{step}: 测试出错了！")

    # 堆栈跟踪
    # logger.error(f"Stack trace: {exception.__traceback__}\n")
    # 截图
    page = RunConfig.page
    if page:
        logger.debug(f"{page}： 开始进行截图操作......")
        browser_dir = os.path.join(IMG_DIR, RunConfig.browser)
        os.makedirs(browser_dir, exist_ok=True)
        file_name = feature_name + "_" + scenario_name + "_" + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + ".png"
        img_path = os.path.join(browser_dir, file_name)
        page.screenshot(path=img_path)
        if img_path:
            #  报错截图添加到allure-pytest报告
            allure_step(step_title="点击查看失败截图......", content=f"{feature_name}-{scenario_name}-{step_name}: 测试出错了！",
                        source=img_path)


def pytest_bdd_before_scenario(request, feature, scenario):
    """
    在执行场景之前调用。可以在此钩子中执行任何预处理操作。它接收 request 对象、feature 对象和 scenario 对象作为参数。
    :param request:
    :param feature:
    :param scenario:
    :return:
    """
    feature_name = getattr(feature, "name", None)
    scenario_name = getattr(scenario, "name", None)
    allure_title(title=f"{feature_name}-{scenario_name}")


# ------------------------------------- END: pytest-bdd钩子函数处理---------------------------------------#

# ------------------------------------- START: pytest钩子函数处理---------------------------------------#
def pytest_terminal_summary(terminalreporter, config):
    """
    收集测试结果
    """
    _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])
    try:
        # 获取pytest传参--reruns的值
        reruns_value = int(config.getoption("--reruns"))
        _RERUN = int(_RERUN / reruns_value)
    except Exception:
        reruns_value = "未配置--reruns参数"
        _RERUN = len([i for i in terminalreporter.stats.get('rerun', []) if i.when != 'teardown'])

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _XPASSED = len([i for i in terminalreporter.stats.get('xpassed', []) if i.when != 'teardown'])
    _XFAILED = len([i for i in terminalreporter.stats.get('xfailed', []) if i.when != 'teardown'])

    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    logger.success(f"\n======================================================\n"
                   "-------------测试结果--------------------\n"
                   f"用例总数: {_TOTAL}\n"
                   f"跳过用例数: {_SKIPPED}\n"
                   f"实际执行用例总数: {_PASSED + _FAILED + _XPASSED + _XFAILED}\n"
                   f"通过用例数: {_PASSED}\n"
                   f"异常用例数: {_ERROR}\n"
                   f"失败用例数: {_FAILED}\n"
                   f"重跑的用例数(--reruns的值): {_RERUN}({reruns_value})\n"
                   f"意外通过的用例数: {_XPASSED}\n"
                   f"预期失败的用例数: {_XFAILED}\n\n"
                   "用例执行时长: %.2f" % _TIMES + " s\n")
    print(f"\n======================================================\n"
          "-------------测试结果--------------------\n"
          f"用例总数: {_TOTAL}\n"
          f"跳过用例数: {_SKIPPED}\n"
          f"实际执行用例总数: {_PASSED + _FAILED + _XPASSED + _XFAILED}\n"
          f"通过用例数: {_PASSED}\n"
          f"异常用例数: {_ERROR}\n"
          f"失败用例数: {_FAILED}\n"
          f"重跑的用例数(--reruns的值): {_RERUN}({reruns_value})\n"
          f"意外通过的用例数: {_XPASSED}\n"
          f"预期失败的用例数: {_XFAILED}\n\n"
          "用例执行时长: %.2f" % _TIMES + " s\n")
    try:
        _RATE = _PASSED / (_TOTAL - _SKIPPED) * 100
        logger.success(
            f"\n用例成功率: %.2f" % _RATE + " %\n"
                                       "=====================================================")
        print(f"\n用例成功率: %.2f" % _RATE + " %\n"
                                         "=====================================================")
    except ZeroDivisionError:
        logger.critical(
            f"用例成功率: 0.00 %\n"
            "=====================================================")
        print(f"用例成功率: 0.00 %\n"
              "=====================================================")

# ------------------------------------- END: pytest钩子函数处理---------------------------------------#
