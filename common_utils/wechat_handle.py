# -*- coding: utf-8 -*-
# @Time    : 2023/5/11 15:01
# @Author  : chenyinhua
# @File    : wechat_handle.py
# @Software: PyCharm
# @Desc: 企业微信机器人

# 标准库导入
import os
import base64
import hashlib
import re
# 第三方库导入
from requests import request
from loguru import logger
# 本地应用/模块导入


class WechatBot:
    """
    企业微信机器人
    当前自定义机器人支持文本（text）、markdown（markdown）、图片（image）、图文（news）, 文件（file）五种消息类型。
    机器人的text/markdown类型消息支持在content中使用<@userid>扩展语法来@群成员
    """

    def __init__(self, webhook_url):
        """
        :param webhook_url: 机器人的WebHook_url
        """
        self.webhook_url = webhook_url
        self.headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

    def send_message(self, payload):
        """
        发送微信消息
        :payload: 请求json数据
        """
        logger.debug("\n======================================================\n" \
                     "-------------Start：发送企业微信消息--------------------\n"
                     f"Webhook_Url: {self.webhook_url}\n" \
                     f"内容: {payload}\n" \
                     "=====================================================")
        response = request(
            url=self.webhook_url,
            json=payload,
            headers=self.headers,
            method="POST"
        )
        if response.json().get("errcode") == 0:
            logger.debug("\n======================================================\n" \
                         "-------------End：发送企业微信消息--------------------\n"
                         f"通过企业微信发送{payload.get('msgtype', '')}消息成功：{response.json()}\n" \
                         "=====================================================")
            print(f"通过企业微信发送{payload.get('msgtype', '')}消息成功：{response.json()}")
            return True
        else:
            logger.error(f"通过企业微信发送{payload.get('msgtype', '')}消息失败：{response.text}")
            print(f"通过企业微信发送{payload.get('msgtype', '')}消息失败：{response.text}")
            return False

    def send_text(self, content, mentioned_list=None, mentioned_mobile_list=None):
        """
        发送文本消息
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_list: userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        """
        payload = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        return self.send_message(payload)

    def send_markdown(self, content):
        """
        发送markdown消息
        目前支持的markdown语法是如下的子集：
            1. 标题 （支持1至6级标题，注意#与文字中间要有空格）
            2. 加粗
            3. 链接
            4. 行内代码段（暂不支持跨行）
            5. 引用
            6. 字体颜色(只支持3种内置颜色), 绿色（color="info"），灰色（color="comment"），橙红色（color="warning"）
        :param content: markdown内容，最长不超过4096个字节，必须是utf8编码
        """
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        return self.send_message(payload)

    def send_picture(self, image_path):
        """
        发送图片消息
        :param image_path: 图片的绝对路径
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        payload = {
            "msgtype": "image",
            "image": {
                "base64": base64.b64encode(image_data).decode("utf-8"),  # # 将图片数据转换成Base64编码格式
                "md5": hashlib.md5(image_data).hexdigest()  # # 计算图片的MD5值
            }
        }
        return self.send_message(payload)

    def send_text_picture(self, articles: list):
        """
        发送图文消息
        :param articles: 图文消息，一个图文消息支持1到8条图文, 包括如下字段
            1. title: 标题，不超过128个字节，超过会自动截断
            2. description: 非必填，描述，不超过512个字节，超过会自动截断
            3. url: 点击后跳转的链接。
            4. picurl: 非必填，图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
        """
        payload = {
            "msgtype": "news",
            "news": {
                "articles": [
                ]
            }
        }
        for article in articles:
            payload["news"]["articles"].append(
                {
                    "title": article.get("title"),
                    "description": article.get("description", ""),
                    "url": article.get("url"),
                    "picurl": article.get("picurl", "")
                }
            )
        return self.send_message(payload)

    def upload_file(self, file_path):
        """
        上传文件到企业微信服务器(要求文件大小在5B~20M之间)
        注意：素材上传得到media_id，该media_id仅三天内有效；media_id只能是对应上传文件的机器人可以使用
        :param file_path: 文件绝对路径
        """
        token_regex = r"key=([\w-]+)"
        match = re.search(token_regex, self.webhook_url)
        token = match.group(1)
        url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={token}&type=file"
        headers = {
            "Content-Type": "multipart/form-data;"
        }
        with open(file_path, "rb") as f:
            files = {"media": (os.path.basename(file_path), f.read())}
        response = request(url=url, method="POST", files=files, headers=headers)
        if response.json().get("errcode") == 0:
            media_id = response.json().get("media_id")
            print(f"上传文件成功，media_id= {media_id}")
            return media_id
        else:
            print(f"上传文件失败：{response.text}")
            return False

    def send_file(self, media_id):
        """
        发送文件
        :param media_id: 文件id，通过下文的文件上传接口获取
        """
        payload = {
            "msgtype": "file",
            "file": {
                "media_id": media_id,
            }
        }
        return self.send_message(payload)
