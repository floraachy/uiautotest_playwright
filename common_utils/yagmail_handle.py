# -*- coding: utf-8 -*-
# @Time    : 2021/8/14 12:21
# @Author  : Flora.Chen
# @File    : yagmail_handle.py
# @Software: PyCharm
# @Desc: 通过第三方模块yagmail发送邮件

# 标准库导入
import os
# 第三方库导入
from loguru import logger
import yagmail
# 本地应用/模块导入


class YagEmailServe:
    def __init__(self, host, user, password):
        """
        user(发件人邮箱), password(邮箱授权码), host(发件人使用的邮箱服务 例如：smtp.163.com)
        """
        self.host = host
        self.user = user
        self.password = password

    def send_email(self, info: dict):
        """
        发送邮件
        :param info:包括,contents(内容), to(收件人列表), subject(邮件标题), attachments(附件列表)
        info = {
            "subject": "",
            "contents": "",
            "to": "",
            "attachments": ""
        }
        :return:
        """
        try:
            logger.debug("\n======================================================\n" \
                         "-------------Start：发送邮件--------------------\n"
                         f"用户名: {self.user}\n" \
                         f"密码: {self.password}\n" \
                         f"host: {self.host}\n" \
                         f"host: {self.host}\n" \
                         f"邮件内容: {info}\n" \
                         "=====================================================")
            yag = yagmail.SMTP(
                user=self.user,
                password=self.password,
                host=self.host)
            # 如果存在附件，则与邮件内容一起发送附件，否则仅发送邮件内容
            if os.path.exists(info['attachments']):
                yag.send(
                    to=info['to'],
                    subject=info['subject'],
                    contents=info['contents'],
                    attachments=info['attachments'])
            else:
                yag.send(
                    to=info['to'],
                    subject=info['subject'],
                    contents=info['contents'])
            yag.close()
            logger.debug("\n======================================================\n" \
                         "-------------End：发送邮件--------------------\n"
                         "发送邮件成功\n" \
                         "=====================================================")
            print("发送邮件成功")
        except Exception as e:
            logger.error(f"发送邮件失败，错误信息: {e}")
            print(f"发送邮件失败，错误信息: {e}")
