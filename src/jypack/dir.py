# -*- coding:gb18030 -*-

import os
import glob

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
        os.system(cmd +  "\"" + f + "\"")

def findSubDirs(dirName):
    """查找dirName目录中的子文件夹"""
    dirList = []
    for d in glob.glob(dirName + "/*"):
        if os.path.isdir(d):
            dirList.append(d)
    return dirList
