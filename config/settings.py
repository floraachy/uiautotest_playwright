# -*- coding: utf-8 -*-
# @Version: Python 3.9
# @Time    : 2023/1/9 17:08
# @Author  : chenyinhua
# @File    : settings.py
# @Software: PyCharm
# @Desc: 项目配置文件
# ------------------------------------ pytest相关配置 ----------------------------------------------------#
class RunConfig:
    """
    运行测试配置
    """
    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = ["chromium"]

    # 运行模式（headless, headed）
    mode = "headless"

    # 窗口大小
    """
    playwright 默认启动的浏览器窗口大小是1280x720， 我们可以通过设置no_viewport参数来禁用固定的窗口大小 ，no_viewport 禁用窗口大小。
    """
    # 这个标识根据具体尺寸设置窗口大小
    window_size = {"width": 1920, "height": 1080}

    # 浏览器页面
    page = None

    # 失败重跑次数
    rerun = 0

    # 失败重跑间隔时间
    reruns_delay = 5

    # 当达到最大失败数，停止执行
    max_fail = "10"


# ------------------------------------ 配置信息 ----------------------------------------------------#
# 0表示默认不发送任何通知， 1代表钉钉通知，2代表企业微信通知， 3代表邮件通知， 4代表所有途径都发送通知
SEND_RESULT_TYPE = 0

# 指定日志收集级别
LOG_LEVEL = None
"""
支持的日志级别：
    None： 表示捕获所有日志
    TRACE: 最低级别的日志级别，用于详细追踪程序的执行。
    DEBUG: 用于调试和开发过程中打印详细的调试信息。
    INFO: 提供程序执行过程中的关键信息。
    SUCCESS: 用于标记成功或重要的里程碑事件。
    WARNING: 表示潜在的问题或不符合预期的情况，但不会导致程序失败。
    ERROR: 表示错误和异常情况，但程序仍然可以继续运行。
    CRITICAL: 表示严重的错误和异常情况，可能导致程序崩溃或无法正常运行。
"""

# ------------------------------------ 邮件配置信息 ----------------------------------------------------#

# 发送邮件的相关配置信息
email = {
    "user": "******",  # 发件人邮箱
    "password": "******",  # 发件人邮箱授权码
    "host": "smtp.qq.com",
    "to": ["******", "******"]  # 收件人邮箱
}

# ------------------------------------ 邮件通知内容 ----------------------------------------------------#
email_subject = f"UI自动化报告"
email_content = """
           各位同事, 大家好:

           自动化用例于 <strong>${start_time} </strong> 开始运行，运行时长：<strong>${run_time} s</strong>， 目前已执行完成。
           ---------------------------------------------------------------------------------------------------------------
           测试人：<strong> ${tester} </strong> 
           所属部门：<strong> ${department} </strong>
           项目环境：<strong> ${run_env} </strong>
           ---------------------------------------------------------------------------------------------------------------
           执行结果如下:
           &nbsp;&nbsp;用例运行总数:<strong> ${total} 个</strong>
           &nbsp;&nbsp;通过用例个数（passed）: <strong><font color="green" >${passed} 个</font></strong>
           &nbsp;&nbsp;失败用例个数（failed）: <strong><font color="red" >${failed} 个</font></strong>
           &nbsp;&nbsp;异常用例个数（error）: <strong><font color="orange" >${broken} 个</font></strong>
           &nbsp;&nbsp;跳过用例个数（skipped）: <strong><font color="grey" >${skipped} 个</font></strong>
           &nbsp;&nbsp;失败重试用例个数 * 次数之和（rerun）: <strong>${rerun} 个</strong>
           &nbsp;&nbsp;成  功   率:<strong> <font color="green" >${pass_rate} %</font></strong>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 钉钉相关配置 ----------------------------------------------------#
ding_talk = {
    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=********",
    "secret": "********"
}

# ------------------------------------ 钉钉通知内容 ----------------------------------------------------#
ding_talk_title = f"UI自动化报告"
ding_talk_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
            ---------------------------------------------------------------------------------------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${run_env} 
           ---------------------------------------------------------------------------------------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）: ${passed} 个
           - 失败用例个数（failed）: ${failed} 个
           - 异常用例个数（error）: ${broken} 个
           - 跳过用例个数（skipped）: ${skipped} 个
           - 失败重试用例个数 * 次数之和（rerun）: ${rerun} 个
           - 成  功   率: ${pass_rate} %

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
wechat = {
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=********",
}
# ------------------------------------ 企业微信通知内容 ----------------------------------------------------#
wechat_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
           --------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${run_env} 
           --------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）:<font color=\"info\"> ${passed} 个</font>
           - 失败用例个数（failed）: <font color=\"warning\"> ${failed}  个</font>
           - 异常用例个数（error）: <font color=\"warning\"> ${broken} 个</font>
           - 跳过用例个数（skipped）: <font color=\"comment\"> ${skipped} 个</font>
           - 失败重试用例个数 * 次数之和（rerun）: <font color=\"comment\"> ${rerun} 个</font>
           - 成  功   率: <font color=\"info\"> ${pass_rate} % </font>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
