# -*- coding:gb18030 -*-

import jypack.string

def replaceTextInFile(file, strDict, encoding="gb18030"):
    """根据strDict提供的字符串字典替换文件中的文本，
    strDict={ "text_old1":"text_new1", "text_old2":"text_new2"}"""
    text = readText(file=file, encoding=encoding)
    result = jypack.string.replaceTextByDict(text=text, strDict=strDict)
    writeText(file=file, text=result, encoding=encoding)

def readText(file, encoding="gb18030"):
    """读取文件的所有文本"""
    f = open(file=file, mode="rt", encoding=encoding)
    result = f.read()
    f.close()
    return result

def writeText(file, text, encoding="gb18030"):
    """写入所有文本到文件"""
    f = open(file=file, mode="wt", encoding=encoding)
    f.write(text)
    f.close()
