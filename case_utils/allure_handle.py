# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 8:58
# @Author  : chenyinhua
# @File    : allure_handle.py
# @Software: PyCharm
# @Desc: 

# 标准库导入
import os
import json
# 第三方库导入
import allure
# 本地应用/模块导入
from config.models import AllureAttachmentType


def allure_title(title: str) -> None:
    """allure中动态生成用例标题"""
    # allure.dynamic动态属性
    allure.dynamic.title(title)


def allure_step(step_title: str, content: str = None, source=None) -> None:
    """
    allure.step()添加测试用例步骤
    :param step_title: 步骤及附件名称
    :param content: 附件内容
    :param source: 文件路径
    """
    if source:
        with allure.step(step_title):
            """
            语法：allure.attach.file(source, name, attachment_type, extension)

            参数解释：
                source：文件路径，相当于传一个文件；
                name：附件名称；
                attachment_type：附件类型，是allure.attachment_type其中的一种；
                extension：附件的扩展名(文件后缀)；
            """
            # 获取上传附件的尾缀，判断对应的 attachment_type 枚举值
            file_suffix = source.split('.')[-1]
            _attachment_type = getattr(AllureAttachmentType, file_suffix.upper(), None)
            allure.attach.file(source=source, name=os.path.basename(source),
                               attachment_type=_attachment_type if _attachment_type is None else _attachment_type.value,
                               extension=file_suffix)
    else:
        with allure.step(step_title):
            """
            语法：allure.attach(body, name, attachment_type, extension)
            参数解释：
                body：要写入附件的内容；
                name：附件名称；
                attachment_type：附件类型，是allure.attachment_type其中的一种；
                extension：附件的扩展名(文件后缀)；
            -------------------------------------------------------------------
            json.dumps(content, ensure_ascii=False, indent=4)
            ensure_ascii表示的意思是是否要转为ASCII码，如果打开(默认打开True)，那么转为json后中文会变成ASCII编码，如果关闭后中文还是中文，不会变为ASCII编码。
            indent表示间隔的长度
            """
            allure.attach(body=json.dumps(content, ensure_ascii=False, indent=4), name=step_title,
                          attachment_type=allure.attachment_type.TEXT)


class AllureReportBeautiful:
    """
    美化allure测试报告
    """

    def __init__(self, allure_html_path=None, allure_results_path=None):
        """
        @param allure_results_path: allure保存测试结果集目录
        @param allure_html_path: allure生成的html报告的目录
        """
        self.allure_html_path = allure_html_path
        self.allure_results_path = allure_results_path

    # 设置报告窗口的标题
    def set_windows_title(self, new_title):
        """
        设置打开的 Allure 报告的浏览器窗口标题文案
        @param new_title:  需要更改的标题文案 【 原文案为：Allure Report 】
        @return:
        """
        report_title_filepath = os.path.join(self.allure_html_path, "index.html")
        # 定义为只读模型，并定义名称为: f
        with open(report_title_filepath, 'r+', encoding="utf-8") as f:
            # 读取当前文件的所有内容
            all_the_lines = f.readlines()
            f.seek(0)
            f.truncate()
            # 循环遍历每一行的内容，将 "Allure Report" 全部替换为 → new_title(新文案)
            for line in all_the_lines:
                f.write(line.replace("Allure Report", new_title))
            # 关闭文件
            f.close()

    def set_report_name(self, new_name):
        """
        修改Allure报告Overview的标题文案
        @param new_name:  需要更改的标题文案 【 原文案为：ALLURE REPORT 】
        @return:
        """
        title_filepath = os.path.join(self.allure_html_path, "widgets", "summary.json")
        # 读取summary.json中的json数据，并改写reportName
        with open(title_filepath, 'rb') as f:
            # 加载json文件中的内容给params
            params = json.load(f)
            # 修改内容
            params['reportName'] = new_name
            # 将修改后的内容保存在dict中
            new_params = params
        # 往summary.json中，覆盖写入新的json数据
        with open(title_filepath, 'w', encoding="utf-8") as f:
            json.dump(new_params, f, ensure_ascii=False, indent=4)

    def set_report_env_on_results(self, env_info):
        """
        在allure-results报告的根目录下生成一个写入了环境信息的文件：environment.properties(注意：不能放置中文，否则会出现乱码)
        @param env_info:  需要写入的环境信息
        @return:
        """

        with open(os.path.join(self.allure_results_path, "environment.properties"), 'w', encoding="utf-8") as f:
            for k, v in env_info.items():
                f.write('{}={}\n'.format(k, v))

    def set_report_env_on_html(self, env_info: dict):
        """
         在allure-html报告中往widgets/environment.json中写入环境信息,
            格式参考如下：[{"values":["Auto Test Report"],"name":"report_title"},{"values":["autotestreport_"]]
        """
        envs = []
        for k, v in env_info.items():
            envs.append({
                "name": k,
                "values": [v]
            })
        with open(os.path.join(self.allure_html_path, "widgets", "environment.json"), 'w', encoding="utf-8") as f:
            json.dump(envs, f, ensure_ascii=False, indent=4)


def allure_logo_change(allure_path, logo_path):
    """
    修改allure的logo
    步骤：
    1. 进入‘allure-x.x.x\config’ 目录，打开 ‘allure.yml’ 文件，在最下面增加一行 ‘- custom-logo-plugin ' ， 特别要注意层级关系。
    2. 复制logo到‘allure-x.x.x\plugins\custom-logo-plugin\static’ 文件夹
    3. 修改‘allure-x.x.x\plugins\custom-logo-plugin\static\styles.css’  文件 来配置logo，参考如下：
    .side-nav__brand {
      background: url('logo.svg') no-repeat left center !important;
      margin-left: 10px;
      height: 65px;
      width: 150px;
      background-size: contain !important;
    }
    .side-nav__brand span{
        display: none;
    }
    @param allure_path:  logo绝对路径
    @param logo_path:  logo绝对路径
    """
    # TODO 后续支持通过代码实现修改
    pass
