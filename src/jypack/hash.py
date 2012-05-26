# -*- coding:gb18030 -*-

import hashlib

def md5String(text = "", encoding = "gb18030"):
    """计算字符串的md5值，字符串的默认编码是gb18030"""
    md5 = hashlib.md5()
    md5.update(bytearray(text.encode(encoding = encoding)))
    return md5.hexdigest()
