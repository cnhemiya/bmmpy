# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:12

@brief 网络 http 相关
"""


import urllib.request
import re
from typeguard import typechecked


@typechecked
def get_data_by_re(url: str, re_str: str) -> list[str]:
    """
    从指定 URL 中根据给定的正则表达式提取数据

    Args:
        url (str): 要访问的 URL
        re_str (str): 正则表达式，用于匹配数据

    Returns:
        list[str]: 匹配到的数据列表

    Examples:
        >>> get_data_by_re("https://example.com", r"\\d+")
        ['123', '456']
    """
    html = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    data = re.findall(re_str, html)
    return data


@typechecked
def download_data(url: str, file_name: str) -> None:
    """
    从指定 URL 下载数据并保存到文件

    Args:
        url (str): 要下载数据的 URL
        file_name (str): 保存数据的文件名

    Returns:
        None
    """
    with open(file_name, "wb+") as fn:
        data = urllib.request.urlopen(url, timeout=60).read()
        fn.write(data)
