# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:09
# @Author  : chenyinhua
# @File    : run.py
# @Software: PyCharm
# @Desc: 框架主入口
"""
说明：
1、用例创建原则，测试文件名必须以“test”开头，测试函数必须以“test”开头。
2、运行方式：
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -m demo 在test环境仅运行打了标记demo用例， 默认报告采用allure
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -browser webkit 使用webkit浏览器运行测试用例
  > python run.py -browser chromium webkit 使用chromium和webkit浏览器运行测试用例
"""
# 标准库导入
import os
import argparse
# 第三方库导入
import pytest
from loguru import logger
# 本地应用/模块导入
from config.settings import LOG_LEVEL, RunConfig
from config.global_vars import GLOBAL_VARS, ENV_VARS
from config.path_config import REPORT_DIR, LOG_DIR, CONF_DIR, LIB_DIR, ALLURE_RESULTS_DIR, \
    ALLURE_HTML_DIR
from case_utils.platform_handle import PlatformHandle
from case_utils.send_result_handle import send_result
from case_utils.allure_handle import AllureReportBeautiful
from common_utils.files_handle import zip_file, copy_file


def capture_logs(level=LOG_LEVEL):
    logger.remove(handler_id=None)  # 清除之前的设置
    logger.info("""
                        _    _         _      _____         _
         __ _ _ __ (_)  / \\  _   _| |_ __|_   _|__  ___| |_
        / _` | "_ \\| | / _ \\| | | | __/ _ \\| |/ _ \\/ __| __|
       | (_| | |_) | |/ ___ \\ |_| | || (_) | |  __/\\__ \\ |_
        \\__,_| .__/|_/_/   \\_\\__,_|\\__\\___/|_|\\___||___/\\__|
             |_|
             Starting      ...     ...     ...
           """)
    if level:
        # 仅捕获指定级别日志
        # 设置生成日志文件，utf-8编码，每天0点切割，zip压缩，保留3天，异步写入
        logger.add(sink=os.path.join(LOG_DIR, "runtime_{time}.log"),
                   level=LOG_LEVEL.upper(),
                   rotation="00:00",
                   retention="3 days",
                   compression="zip",
                   encoding="utf-8",
                   enqueue=True,
                   format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}")
    else:
        # 捕获所有日志
        logger.add(
            sink=os.path.join(LOG_DIR, "runtime_{time}_all.log"),
            enqueue=True,
            encoding="utf-8",
            retention="3 days",
            compression="zip",
            rotation="00:00",
            format="{time:YYYY-MM-DD HH:mm:ss} {level} From {module}.{function} : {message}",
        )


def run(**kwargs):
    try:
        # ------------------------ 处理一下获取到的参数----------------------------
        env_key = kwargs.get("env", "") or None
        mark = kwargs.get("m", "") or None
        browser = kwargs.get("browser", "") or None
        RunConfig.browser = browser if browser else RunConfig.browser
        mode = kwargs.get("mode", "") or None
        RunConfig.mode = mode.lower() if mode else RunConfig.mode
        # ------------------------ 捕获日志----------------------------
        capture_logs()
        # ------------------------ 设置pytest相关参数 ------------------------
        arg_list = [f"--maxfail={RunConfig.max_fail}", f"--reruns={RunConfig.rerun}",
                    f"--reruns-delay={RunConfig.reruns_delay}", f'--alluredir={ALLURE_RESULTS_DIR}',
                    '--clean-alluredir']

        if RunConfig.mode == "headed":
            arg_list.append("--headed")

        if isinstance(RunConfig.browser, list):
            for browser in RunConfig.browser:
                arg_list.append(f"--browser={browser.lower()}")
                # arg_list.extend(["--browser", f"{browser.lower()}"])

        if isinstance(RunConfig.browser, str):
            arg_list.append(f"--browser {RunConfig.browser.lower()}")
        if mark:
            arg_list.append(f'-m {mark}')
        # ------------------------ 设置全局变量 ------------------------
        # 根据指定的环境参数，将运行环境所需相关配置数据保存到GLOBAL_VARS
        GLOBAL_VARS["env_key"] = env_key
        if ENV_VARS.get(env_key.lower()):
            GLOBAL_VARS.update(ENV_VARS[env_key.lower()])
        # ------------------------ pytest执行测试用例 ------------------------
        print(f"打印一下运行的参数：{arg_list}")
        pytest.main(args=arg_list)
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 定义命令行参数
    parser = argparse.ArgumentParser(description="框架主入口")
    parser.add_argument("-env", default="test", help="输入运行环境：test 或 live")
    parser.add_argument("-m", default=None, help="选择需要运行的用例：python.ini配置的名称")
    parser.add_argument("-browser", default=None, nargs='*',
                        help="浏览器驱动类型配置，支持如下类型：chromium, firefox, webkit")
    parser.add_argument("-mode", default=None, nargs='*',
                        help="浏览器驱动类型配置，支持如下类型：headless, headful")
    args = parser.parse_args()
    run(**vars(args))

"""
pytest相关参数：以下也可通过pytest.ini配置
     --reruns: 失败重跑次数
     --reruns-delay 失败重跑间隔时间
     --count: 重复执行次数
    -v: 显示错误位置以及错误的详细信息
    -s: 等价于 pytest --capture=no 可以捕获print函数的输出
    -q: 简化输出信息
    -m: 运行指定标签的测试用例
    -x: 一旦错误，则停止运行
    --maxfail: 设置最大失败次数，当超出这个阈值时，则不会在执行测试用例
    "--reruns=3", "--reruns-delay=2"
    -s：这个选项表示关闭捕获输出，即将输出打印到控制台而不是被 pytest 截获。这在调试测试时很有用，因为可以直接查看打印的输出。

    --cache-clear：这个选项表示在运行测试之前清除 pytest 的缓存。缓存包括已运行的测试结果等信息，此选项可用于确保重新执行所有测试。

    --capture=sys：这个选项表示将捕获标准输出和标准错误输出，并将其显示在 pytest 的测试报告中。

    --self-contained-html：这个选项表示生成一个独立的 HTML 格式的测试报告文件，其中包含了所有的样式和资源文件。这样，您可以将该文件单独保存，在没有其他依赖的情况下查看测试结果。

    --reruns=0：这个选项表示在测试失败的情况下不重新运行测试。如果设置为正整数，例如 --reruns=3，会在测试失败时重新运行测试最多 3 次。

    --reruns-delay=5：这个选项表示重新运行测试的延迟时间，单位为秒。默认情况下，如果使用了 --reruns 选项，pytest 会立即重新执行失败的测试。如果指定了 --reruns-delay，pytest 在重新运行之前会等待指定的延迟时间。

    -p no:faulthandler 是 pytest 的命令行选项之一，用于禁用 pytest 插件 faulthandler。

    faulthandler 是一个 pytest 插件，它用于跟踪和报告 Python 进程中的崩溃和异常情况。它可以在程序遇到严重错误时打印堆栈跟踪信息，并提供一些诊断功能。

    使用 -p no:faulthandler 选项可以禁用 faulthandler 插件的加载和运行。这意味着 pytest 将不会使用该插件来处理和报告崩溃和异常情况。如果您确定不需要 faulthandler 插件的功能，或者遇到与其加载有关的问题，可以使用这个选项来禁用它。

    请注意，-p no:faulthandler 选项只会禁用 faulthandler 插件，其他可能存在的插件仍然会正常加载和运行。如果您想禁用所有插件，可以使用 -p no:all 选项。

 allure相关参数：
    –-alluredir这个选项用于指定存储测试结果的路径
"""
