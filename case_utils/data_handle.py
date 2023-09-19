# 标准库导入
import random
import re
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
    def remove_special_characters(cls, target:str):
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


def data_handle(obj, source):
    """
    递归处理字典、列表中的字符串，将${}占位符替换成source中的值
    """
    obj = eval_data_process(obj)
    if isinstance(obj, str):
        # 寻找${}， 在source中找到对应的关键字进行替换，如obj=${user_id}, 去寻找source中对应键user_id的值（假设user_id=1），使得obj=1
        obj = Template(obj).safe_substitute(source)
        # 寻找${python表达式}， 将Python表达式eval得出其具体值
        for func in re.findall('\\${(.*?)}', obj):
            """
            兼容一下如下数据处理：faker.name().replace(" ", "").replace(".", "")
            faker是FakerData()中的实例变量。
            """
            if func.startswith("faker."):
                # 英文的faker数据：self.faker = Faker()
                faker = FakerData().faker
                obj = obj.replace('${%s}' % func, eval(func))
            elif func.startswith("fk_zh."):
                # 中文的faker数据： self.fk_zh = Faker(locale='zh_CN')
                fk_zh = FakerData().fk_zh
                obj = obj.replace('${%s}' % func, eval(func))
            else:
                # 这里获取到的func是这样的格式，例如random_int()， 但实际我们通过FakerData()获取到的方法是这样的格式，例如random_int, 所以我们需要进行处理
                func_name = func.split("(")[0] if "(" in func else func
                if hasattr(FakerData(), func_name) and callable(getattr(FakerData(), func_name)):
                    # 调用FakerData类的方法获取数据
                    obj = obj.replace('${%s}' % func, str(getattr(FakerData(), func_name)()))
            # 处理其他Python表达式，例如：${1+1}
            obj = obj.replace('${%s}' % func, func)
            obj = eval_data_process(obj)
            return obj
        return eval_data_process(obj)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            obj[index] = data_handle(item, source)
        return obj

    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = data_handle(value, source)
        return obj

    else:
        return obj


# 将"[1,2,3]" 或者"{'k':'v'}" -> [1,2,3], {'k':'v'}
def eval_data(data):
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


def eval_data_process(data):
    """
    将数据中的字符串表达式处理后更新其值为表达式
    """
    # 如果目标数据是字符串，直接尝试eval
    if isinstance(data, str):
        data = eval_data(data)
    # 如果目标数据是列表，遍历列表的每一个数据，再用递归的方法处理每一个item
    if isinstance(data, list):
        for index, item in enumerate(data):
            data[index] = eval_data_process(eval_data(item))
    # 如果目标数据是字典，遍历字典的每一个值，再用递归的方法处理每一个value
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = eval_data_process(eval_data(value))
    return data
