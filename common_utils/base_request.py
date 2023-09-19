# -*- coding: utf-8 -*-
# @Time    : 2023/6/22 14:11
# @Author  : chenyinhua
# @File    : base_request.py
# @Software: PyCharm
# @Desc: 封装的requests模块

# 标准库导入
import time
from typing import Dict, Union
# 第三方库导入
import requests
from loguru import logger
from requests import Response
from requests_toolbelt import MultipartEncoder


# 本地应用/模块导入


class BaseRequest:
    """
    进行请求
    """

    TIMEOUT = 5

    session = None

    @classmethod
    def get_session(cls):
        """
        单例模式保证测试过程中使用的都是一个session对象；
        requests.session可以自动处理cookies，做状态保持。
        """
        if cls.session is None:
            cls.session = requests.Session()
        return cls.session

    @classmethod
    def send_request(cls, req_data: Dict[str, Union[str, Dict, MultipartEncoder]]) -> Response:
        """
        处理请求数据，转换成可用数据发送请求
        :param req_data: 请求数据
        :return: 响应对象
        """
        try:
            logger.debug("\n" + "=" * 80
                         + "\n-------------Start：请求前--------------------\n"
                           f"用例标题: {req_data.get('title', None)}\n"
                           f"请求路径: {req_data.get('url', None)}\n"
                           f"请求方式: {req_data.get('method', None)}\n"
                           f"请求头:   {req_data.get('headers', None)}\n"
                           f"请求Cookies:   {req_data.get('cookies', None)}\n"
                           f"请求关键字: {req_data.get('request_type', None)}\n"
                           f"请求内容: {req_data.get('payload', None)}\n"
                           f"请求文件: {req_data.get('files', None)}\n"
                         + "=" * 80)
            print("\n" + "=" * 80
                  + "\n-------------Start：请求前--------------------\n"
                    f"用例标题: {req_data.get('title', None)}\n"
                    f"请求路径: {req_data.get('url', None)}\n"
                    f"请求方式: {req_data.get('method', None)}\n"
                    f"请求头:   {req_data.get('headers', None)}\n"
                    f"请求Cookies:   {req_data.get('cookies', None)}\n"
                    f"请求关键字: {req_data.get('request_type', None)}\n"
                    f"请求内容: {req_data.get('payload', None)}\n"
                    f"请求文件: {req_data.get('files', None)}\n"
                  + "=" * 80)
            res = cls.send_api_request(
                url=req_data.get("url"),
                method=req_data.get("method").lower(),
                request_type=req_data.get("request_type", None),
                header=req_data.get("headers", None),
                payload=req_data.get("payload", None),
                files=req_data.get("files", None),
                cookies=req_data.get("cookies", None)
            )
            logger.debug("\n" + "=" * 80
                         + "\n-------------End：请求后--------------------\n"
                           f"响应数据: {res.text}\n"
                           f"响应码: {res.status_code}\n"
                         + "=" * 80)
            print("\n" + "=" * 80
                  + "\n-------------End：请求后--------------------\n"
                    f"响应数据: {res.text}\n"
                    f"响应码: {res.status_code}\n"
                  + "=" * 80)
        except requests.exceptions.RequestException as e:
            logger.error(f"请求出错，{str(e)}")
            print(f"请求出错，{str(e)}")
            raise ValueError(f"请求出错，{str(e)}")

        return res

    @classmethod
    def send_api_request(cls, url: str, method: str, request_type: str, header: Dict[str, str] = None, payload=None,
                         files=None, cookies=None) -> Response:
        """
        发送请求
        :param method: 请求方法
        :param url: 请求url
        :param request_type: 请求参数类型，可选值为params，json，data
        :param payload: 请求数据，对于不同请求类型，可以为dict，MultipartEncoder等
        :param files: 请求上传的文件
        :param header: 请求头
        :param cookies: 请求cookies
        :return: 返回res对象
        """
        headers = header or {}
        session = cls.get_session()

        if request_type:
            if request_type.lower() == 'params':
                res = session.request(method=method, url=url, params=payload, headers=headers, cookies=cookies,
                                      timeout=cls.TIMEOUT)
                return res
            elif request_type.lower() == 'data':
                res = session.request(method=method, url=url, data=payload, headers=headers, cookies=cookies,
                                      timeout=cls.TIMEOUT)
                return res
            elif request_type.lower() == 'json':
                res = session.request(method=method, url=url, json=payload, headers=headers, cookies=cookies,
                                      timeout=cls.TIMEOUT)
                return res
            elif request_type.lower() == 'file':
                if files:
                    if payload:
                        if isinstance(files, dict):
                            for k, v in payload.items():
                                files[k] = v
                        elif isinstance(files, list):
                            # TODO 这里是应对多文件上传的情况，暂时没有接口帮助验证是否真正上传了多个文件，有可能只上传成功了一个
                            for k, v in payload.items():
                                files.append((k, v))
                    encoder = MultipartEncoder(fields=files, boundary='------------------------' + str(time.time()))
                    headers['Content-Type'] = encoder.content_type
                    res = session.request(method=method, url=url, data=encoder.to_string(), headers=headers,
                                          cookies=cookies, timeout=cls.TIMEOUT)
                    return res
                else:
                    logger.error('上传的文件不能为空')
                    print('上传的文件不能为空')
            else:
                logger.error('request_type可选关键字为params, json, data, file')
                print('request_type可选关键字为params, json, data, file')
                raise ValueError('request_type可选关键字为params, json, data, file')
        else:
            logger.error('request_type参数不能为空')
            print('request_type参数不能为空')
            raise ValueError('request_type参数不能为空')
