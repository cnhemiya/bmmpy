# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:10

@brief 哈希计算相关
"""

import hashlib
from typeguard import typechecked


@typechecked
def md5_string(text: str = "", encoding: str = "utf-8") -> str:
    """
    计算字符串的 MD5 值。

    Args:
        text (str): 要计算 MD5 的字符串，默认为空字符串。
        encoding (str): 字符串的编码，默认为 "utf-8"。

    Returns:
        str: 计算得到的 MD5 值的十六进制表示。

    Raises:
        TypeError: 当 text 不是字符串类型时抛出。
        LookupError: 当 encoding 无效时抛出。

    Examples:
        >>> md5_string("hello")
        '5d41402abc4b2a76b9719d911017c593'
        >>> md5_string("", "utf-8")
        'd41d8cd98f00b204e9800998ecf8427e'
    """
    md5 = hashlib.md5()
    md5.update(bytearray(text.encode(encoding=encoding)))
    return md5.hexdigest()
