# -*- coding: utf-8 -*-

import urllib.request
import re

def getDataByRe(url, reStr):
    """从 url 根据给定正则返回数据"""
    html = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    data = re.findall(reStr, html)
    return data

def downLoadData(url, fileName):
    """从 url 下载数据并保存"""
    fn = open(fileName, "wb+")
    data = urllib.request.urlopen(url, timeout=60).read()
    fn.write(data)
    fn.close()