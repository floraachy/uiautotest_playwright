# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 15:22
# @Author  : chenyinhua
# @File    : models.py
# @Software: PyCharm
# @Desc:

# 标准库导入
from enum import Enum, unique  # python 3.x版本才能使用


class NotificationType(Enum):
    """ 自动化通知方式 """
    DEFAULT = 0
    DING_TALK = 1
    WECHAT = 2
    EMAIL = 3
    ALL = 4


@unique  # 枚举类装饰器，确保只有一个名称绑定到任何一个值。
class AllureAttachmentType(Enum):
    """
    allure 报告的文件类型枚举
    """
    TEXT = "txt"
    CSV = "csv"
    TSV = "tsv"
    URI_LIST = "uri"

    HTML = "html"
    XML = "xml"
    JSON = "json"
    YAML = "yaml"
    PCAP = "pcap"

    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    GIF = "gif"
    BMP = "bmp"
    TIFF = "tiff"

    MP4 = "mp4"
    OGG = "ogg"
    WEBM = "webm"

    PDF = "pdf"
