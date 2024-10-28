# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:16

@brief 字符串相关
"""


def replace_string_by_dict(string_: str, str_dict: dict):
    """
    根据提供的字符串字典替换文本

    Args:
        string_ (str): 要替换的原始字符串
        str_dict (dict): 字符串字典，格式为 {"str_old1": "str_new1", "str_old2": "str_new2"}

    Returns:
        str: 替换后的字符串
    """
    for key in str_dict:
        string_ = string_.replace(key, str_dict[key])
    return string_


def str2int_list(str_list: str, sep=","):
    """
    将字符串转换为整型列表。

    Args:
        str_list: 由整数字符串组成的字符串，例如 "1,2,3,4"
        sep: 分隔符，默认为逗号 ","

    Returns:
        一个包含整数的列表，例如 [1, 2, 3, 4]

    Raises:
        ValueError: 如果字符串中的任何元素不能转换为整型
    """
    int_list = []
    for item in str_list.split(sep):
        try:
            int_list.append(int(item))
        except ValueError:
            raise ValueError(f"无法将字符串 '{item}' 转换为整型")
    return int_list
