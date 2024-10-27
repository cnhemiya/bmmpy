# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:16

@brief 字符串相关
"""


def replace_string_by_dict(string_, str_dict):
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
