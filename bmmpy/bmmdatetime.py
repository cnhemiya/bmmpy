# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:06

@brief 日期时间相关
"""

import datetime


def now_time_str():
    """
    获取当前时间，并格式化为字符串

    Returns:
        str: 当前时间的字符串表示，格式为 "YYYY-MM-DD HH:MM:SS"
    """
    today = datetime.datetime.today()
    return today.strftime("%Y-%m-%d %H:%M:%S")
