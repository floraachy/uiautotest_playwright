# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 16:26
# @Author  : chenyinhua
# @File    : platform_handle.py
# @Software: PyCharm
# @Desc:  跨平台的支持allure，用于生成allure测试报告

# 标准库导入
import platform


class PlatformHandle:
    """跨平台的支持allure, webdriver"""

    @property
    def allure(self):
        if platform.system() == "Windows":
            cmd = "allure.bat"
            # 生成测试报告 --clean 覆盖路径，将上次的结果覆盖掉
            cmd2 = "{} generate {} -o {} --clean"
        else:
            cmd = "allure"
            # 生成测试报告 --clean 覆盖路径，将上次的结果覆盖掉
            cmd2 = "sudo {} generate {} -o {} --clean"
        return cmd, cmd2


if __name__ == '__main__':
    plat = PlatformHandle()
    res = plat.allure[0]
    print(res)
