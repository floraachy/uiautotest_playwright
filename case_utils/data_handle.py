# -*- coding: utf-8 -*-
# @Time    : 2023/9/21 17:20
# @Author  : chenyinhua
# @File    : data_handle.py
# @Software: PyCharm
# @Desc:

# 标准库导入
import random
import re, uuid
from datetime import datetime, date, timedelta
# 第三方库导入
from faker import Faker
from string import Template


class FakerData:
    """
    测试数据生成类
    """

    def __init__(self):
        self.fk_zh = Faker(locale='zh_CN')
        self.faker = Faker()

    @classmethod
    def generate_random_int(cls, *args) -> int:
        """
        :return: 随机数
        """
        # 检查是否传入了参数
        if not args:
            # 没有传参，就从5000内随机取一个整数返回
            return random.randint(0, 5000)

        # 排序参数并获取最小值和最大值
        min_val = min(args)
        max_val = max(args)

        # 生成并返回随机整数
        return random.randint(min_val, max_val)

    def generate_phone(self, lan="en") -> int:
        """
        :return: 随机生成手机号码
        """
        if lan == "zh":
            phone = self.fk_zh.phone_number()
        else:
            phone = self.faker.phone_number()
        return phone

    def generate_id_number(self, lan="en") -> int:
        """

        :return: 随机生成身份证号码
        """
        if lan == "zh":
            id_number = self.fk_zh.ssn()
        else:
            id_number = self.faker.ssn()
        return id_number

    def generate_female_name(self, lan="en") -> str:
        """

        :return: 女生姓名
        """
        if lan == "zh":
            female_name = self.fk_zh.name_female()
        else:
            female_name = self.faker.name_female()
        return female_name

    def generate_male_name(self, lan="en") -> str:
        """

        :return: 男生姓名
        """
        if lan == "zh":
            male_name = self.fk_zh.name_male()
        else:
            male_name = self.faker.name_male()
        return male_name

    def generate_name(self, lan="en") -> str:
        """

        :return: 人名
        """
        if lan == "zh":
            name = self.fk_zh.name()
        else:
            name = self.faker.name()
        return name

    def generate_email(self, lan="en") -> str:
        """

        :return: 生成邮箱
        """
        if lan == "zh":
            email = self.fk_zh.email()
        else:
            email = self.faker.email()
        return email

    def generate_identifier(self, lan="en"):
        """
        :return:生成随机标识，满足要求：长度为2~100， 只能包含数字，字母，下划线(_)，中划线(-)，英文句号(.)，必须以数字和字母开头，不能以下划线/中划线/英文句号开头和结尾
        """
        if lan == "zh":
            fk = self.fk_zh
        else:
            fk = self.faker
        while True:
            identifier = fk.slug()  # 生成随机的slug标识

            if (
                    re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,98}[a-zA-Z0-9]$', identifier) and
                    not (identifier.startswith('_') or identifier.startswith('-') or identifier.startswith('.')) and
                    not (identifier.endswith('_') or identifier.endswith('.'))
            ):
                return identifier

    @classmethod
    def generate_time(cls, fmt='%Y-%m-%d %H:%M:%S') -> str:
        """
        计算当前时间
        :return:
        """
        now_time = datetime.now().strftime(fmt)
        return now_time

    @classmethod
    def generate_today_date(cls):
        """获取今日0点整时间"""

        _today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(_today)

    @classmethod
    def generate_time_after_week(cls):
        """获取一周后12点整的时间"""

        _time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return _time_after_week

    @classmethod
    def remove_special_characters(cls, target: str):
        """
        移除字符串中的特殊字符。
        在Python中用replace()函数操作指定字符
        常用字符unicode的编码范围：
        数字：\u0030-\u0039
        汉字：\u4e00-\u9fa5
        大写字母：\u0041-\u005a
        小写字母：\u0061-\u007a
        英文字母：\u0041-\u007a
        """
        pattern = r'([^\u4e00-\u9fa5])'
        result = re.sub(pattern, '', target)
        return result


class DataHandle:
    def __init__(self):
        # 实例化FakerData类，避免反复实例，提高性能。
        self.FakerDataClass = FakerData()
        # 获取FakerData类所有自定义方法
        self.method_list = [method for method in dir(FakerData) if
                            callable(getattr(FakerData, method)) and not method.startswith("__")]
        self.should_print = True

    # 将"[1,2,3]" 或者"{'k':'v'}" -> [1,2,3], {'k':'v'}
    def eval_data(self, data):
        """
        执行一个字符串表达式，并返回其表达式的值
        """
        try:
            if hasattr(eval(data), "__call__"):
                return data
            else:
                return eval(data)
        except Exception:
            return data

    def replace_and_store_placeholders(self, pattern, text):
        """
        提取字符串中符合正则表达式的元素，同时用一个唯一的uuid来替换原有字符串
        例如：
        原字符串：user_id: ${user_id}, user_name: ${user_name}
        替换后的原字符串：user_id: e1c6fc74-2f21-49a9-8d0c-de16650c6364, user_name: 50c74155-5cb5-4809-bc5d-277addf8c3e7
        暂存的需要被处理的关键字或函数：{'e1c6fc74-2f21-49a9-8d0c-de16650c6364': {0: '${user_id}', 1: 'user_id'}, '50c74155-5cb5-4809-bc5d-277addf8c3e7': {0: '${user_name}', 1: 'user_name'}}
        """
        placeholders = {}

        def replace(match):
            placeholder = str(uuid.uuid4())  # 使用uuid生成唯一的占位符
            placeholders[placeholder] = {0: match.group(0), 1: match.group(1)}  # 将提取到的字符串存储到字典中
            return placeholder

        # 使用正则表达式进行字符串匹配和替换，同时指定替换次数为 1
        replaced_text = re.sub(pattern, replace, text, count=1)
        while replaced_text != text:
            text = replaced_text
            replaced_text = re.sub(pattern, replace, text, count=1)
        return replaced_text, placeholders

    def data_handle(self, obj, source=None):
        """
        递归处理字典、列表中的字符串，将${}占位符替换成source中的值
        """
        func = {}
        keys = {}
        if not source or not isinstance(source, dict):
            print("source为空或者source不是字典格式，都将认为是：{}")
            source = {}
        # 如果进来的是字符串，先将各种类型的表达式处理完
        if isinstance(obj, str):
            # 先把python表达式找出来存着，这里会漏掉一些诸如1+1的表达式
            pattern = r"\${([^}]+\))}"  # 匹配以 "${" 开头、以 ")}" 结尾的字符串，并在括号内提取内容，括号内不能包含"}"字符
            obj, func = self.replace_and_store_placeholders(pattern, obj)
            # 再把关键字替换的找出来存着，这里会将1+1这样的表达式存起来
            pattern = r'\$\{([^}]+)\}'  # 定义匹配以"${"开头，"}"结尾的字符串的正则表达式
            obj, keys = self.replace_and_store_placeholders(pattern, obj)
            # 接着处理表达式和关键字替换，先进行关键字替换
            keys = eval(Template(str(keys)).safe_substitute(source))  # 替换并转为字典
            for key, value in keys.items():  # 遍历字典替换
                obj = obj.replace(key, value[0])
            # 再找一遍剩余的${}跟第一步的结果合并，提取漏掉的诸如1+1的表达式(在此认为关键字无法替换的都是表达式，最后表达式也无法处理的情况就报错或者原样返回)
            obj, func_temp = self.replace_and_store_placeholders(pattern, obj)
            func.update(func_temp)
            # 进行函数调用替换
            obj = self.invoke_funcs(obj, func)
            # 把处理后的结果，eval一下
            return self.eval_data(obj)
        elif isinstance(obj, list):
            for index, item in enumerate(obj):
                obj[index] = self.data_handle(item, source)
            return obj
        elif isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = self.data_handle(value, source)
            return obj
        else:
            return obj

    def invoke_funcs(self, obj, funcs):
        """
        调用方法，并将方法返回的结果替换到obj中去
        """
        for key, funcs in funcs.items():  # 遍历方法字典调用并替换
            func = funcs[1]
            # print("invoke func : ", func)
            try:
                if "." in func:
                    if func.startswith("faker."):
                        # 英文的faker数据：self.faker = Faker()
                        faker = self.FakerDataClass.faker
                        obj = obj.replace(key, eval(func))
                    elif func.startswith("fk_zh."):
                        # 中文的faker数据： self.fk_zh = Faker(locale='zh_CN')
                        fk_zh = self.FakerDataClass.fk_zh
                        obj = obj.replace(key, eval(func))
                    else:
                        obj = obj.replace(key, str(eval(func)))
                else:
                    func_parts = func.split('(')
                    func_name = func_parts[0]
                    func_args_str = ''.join(func_parts[1:])[:-1]
                    if func_name in self.method_list:  # 证明是FakerData类方法
                        method = getattr(self.FakerDataClass, func_name)
                        res = eval(f"method({func_args_str})")  # 尝试直接调用
                        obj = obj.replace(key, str(res))
                    else:  # 不是FakerData类方法，但有可能是 1+1 这样的
                        obj = obj.replace(key, str(eval(func)))
            except:
                print("Warn: --------函数：%s 无法调用成功, 请检查是否存在该函数-------" % func)
                obj = obj.replace(key, funcs[0])
                pass

        return obj


# 声明data_handle方法，这样外部就可以直接import data_handle来使用了
data_handle = DataHandle().data_handle

if __name__ == '__main__':
    # 下面是测试代码
    target = {
        "user_id": 1,
        "user_name": "flora",
        "name": "test",
        "age": 17
    }
    # 需要识别${python表达式}，这里random方法是需要导入random包的
    data_01 = "选择.gitignore: ${random.choice(['Ada', 'Actionscript', 'Ansible', 'Android', 'Agda'])}，开源许可证: ${random.choice(['0BSD', 'AAL', 'AFL-1.1', '389-exception'])}"
    # new = data_handle(data_01)
    # print(new, type(new))

    # 这个用到了target
    data_02 = {
        "age": "${generate_random_int()}.",
        "message": "Hello, ${FakerData().generate_female_name()}! Your age is ${age}. Random number: ${FakerData().generate_random_int()}",
        "nested_data": [
            "This is ${name}'s data.",
            {
                "message": "Age: ${age}.",
                "nested_list": [
                    "More data: ${generate_random_int()}",
                ]
            }
        ]
    }
    # new = data_handle(data_02, target)
    # print(new, type(new))

    data_03 = "user_id: ${user_id}, user_name: ${user_name}"
    # new = data_handle(data_03, target)
    # print(new, type(new))

    # 需要识别 字符串里面是python表达式的情况
    data_04 = "[1,2,3,4]"
    # new = data_handle(data_04)
    # print(new, type(new))

    data_05 = "1+1"
    # new = data_handle(data_05)
    # print(new, type(new))

    data_06 = "[1, '1', [1, 2], {'name':'flora', 'age': '1'}]"
    # new = data_handle(data_06)
    # print(new, type(new))

    # 需要识别自定义的函数，同时支持多种，下面两种写法有细微差别
    data_07 = "Hello, ${generate_female_name()}! Random number: ${generate_random_int()}"
    # new = data_handle(data_07)
    # print(new, type(new))

    data_08 = "Hello, ${generate_female_name()}! Random number: ${FakerData().generate_random_int()}"
    # new = data_handle(data_08)
    # print(new, type(new))

    data_09 = "Hello, ${FakerData().generate_female_name()}! Random number: ${FakerData.generate_random_int()}"
    # new = data_handle(data_09)
    # print(new, type(new))

    data_10 = {
        "payload": {
            "startTime": "${FakerData.generate_time('%Y-%m-%d')}",
            "common2": "${faker.name()}",  # 这里是使用类FakerData里面的实例属性faker
            "url": "/api/accounts/${FakerData.generate_time('%Y-%m-%d')} / login.json",
            "fragement": {
                "startTime": "${FakerData.generate_time('%Y-%m-%d')}",
                "common2": "${faker.name()}",  # 这里是使用类FakerData里面的实例属性faker
                "url": "/api/accounts/${FakerData.generate_time('%Y-%m-%d')} / login.json"
            }
        }

    }
    # new = data_handle(data_10)
    # print(new, type(new))

    data_11 = "/api/accounts/${FakerData.generate_time('%Y-%m-%d')}/login.json"
    # new = data_handle(data_11)
    # print(new, type(new))

    # FakerData类中没有封装random_name这个方法，会无法处理
    data_12 = '[[1,2,3,4],"${FakerData().random_name()}"]'
    # new = data_handle(data_12)
    # print(new, type(new))
    # 下面这种写法不是字符串里面，不是正确格式的列表，${FakerData().generate_name()需要用引号包起来，因此无法正确处理成列表，最后返回的是str
    data_13 = '[[1,2,3,4],${FakerData().generate_name()}]'
    # new = data_handle(data_13)
    # print(new, type(new))

    data_15 = '[[1,2,3,4],${FakerData().generate_random_int()}]'
    # new = data_handle(data_15)
    # print(new, type(new))

    # 导入其他方法，也可以直接使用
    # from common_utils.time_handle import test_fun_a
    # data = "${test_fun_a()}"
    # new = data_handle(data)
    # print(new, type(new))

    # 支付方法传参使用
    payload = {
        "name": "${generate_name(lan='zh')}",
        "repository_name": "${generate_name('zh')}",
        "desc": '[[1,2,3,4],"${FakerData().generate_random_int()}"]',
        "pre": '[[1,2,3,4],${FakerData().generate_name()}]'
    }
    # new = data_handle(payload)
    # print(new, type(new))
