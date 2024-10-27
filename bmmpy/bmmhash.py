# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:10

@brief 哈希计算相关
"""

import hashlib


def md5_string(text="", encoding="utf-8"):
    """
    计算字符串的MD5值

    Args:
        text (str): 要计算MD5的字符串，默认为空字符串
        encoding (str): 字符串的编码，默认为 "utf-8"

    Returns:
        str: 计算得到的MD5值的十六进制表示
    """
    md5 = hashlib.md5()
    md5.update(bytearray(text.encode(encoding=encoding)))
    return md5.hexdigest()
