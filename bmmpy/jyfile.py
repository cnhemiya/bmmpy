# -*- coding: utf-8 -*-

import os
import glob
import jypy.jystring


def replaceTextInFile(file, strDict, encoding = "utf-8"):
    """根据strDict提供的字符串字典替换文件中的文本，
    strDict={ "text_old1":"text_new1", "text_old2":"text_new2"}"""
    text = readText(file = file, encoding = encoding)
    result = jypy.jystring.replaceTextByDict(text = text, strDict = strDict)
    writeText(file = file, text = result, encoding = encoding)


def readText(file, encoding = "utf-8"):
    """读取文件的所有文本"""
    f = open(file = file, mode = "rt", encoding = encoding)
    result = f.read()
    f.close()
    return result


def writeText(file, text, encoding = "utf-8"):
    """写入所有文本到文件"""
    f = open(file = file, mode = "wt", encoding = encoding)
    f.write(text)
    f.close()


def findFiles(dirName):
    """用通配符查找dirName目录中的文件，dirName 例如 c:/*"""
    fileList = []
    for fileName in glob.glob(dirName):
        if os.path.isfile(fileName):
            fileList.append(fileName)
    return fileList


def execCmdInFiles(cmd, dirName):
    """查找dirName目录中的文件并执行cmd命令，dirName 例如 c:/*.zip"""
    files = findFiles(dirName)
    for f in files:
        os.system(cmd + "\"" + f + "\"")


def findSubDirs(dirName):
    """查找dirName目录中的子文件夹"""
    dirList = []
    for d in glob.glob(dirName + "/*"):
        if os.path.isdir(d):
            dirList.append(d)
    return dirList

