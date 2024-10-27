# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-10-28 00:15

@brief 文件目录相关
"""

import os
import glob
from bmmpy import bmmstring


def replace_text_in_file(file, str_dict, encoding="utf-8"):
    """
    根据提供的字符串字典替换文件中的文本

    Args:
        file (str): 要操作的文件路径
        str_dict (dict): 字符串字典，格式为 {"text_old1": "text_new1", "text_old2": "text_new2"}
        encoding (str): 文件编码，默认为 "utf-8"

    Returns:
        None
    """
    text = read_text(file=file, encoding=encoding)
    result = bmmstring.replace_string_by_dict(text=text, str_dict=str_dict)
    write_text(file=file, text=result, encoding=encoding)


def read_text(file, encoding="utf-8"):
    """
    读取文件的所有文本内容

    Args:
        file (str): 文件路径
        encoding (str): 文件编码，默认为 "utf-8"

    Returns:
        str: 文件内容
    """
    with open(file=file, mode="rt", encoding=encoding) as f:
        result = f.read()
    return result


def write_text(file, text, encoding="utf-8"):
    """
    将文本写入文件

    Args:
        file (str): 文件路径
        text (str): 要写入的文本内容
        encoding (str): 文件编码，默认为 "utf-8"

    Returns:
        None
    """
    with open(file=file, mode='wt', encoding=encoding) as f:
        f.write(text)


def find_files(dir_name):
    """
    使用通配符查找目录中的文件

    Args:
        dir_name (str): 目录路径，例如 "c:/*"

    Returns:
        list: 找到的文件列表
    """
    file_list = []
    for file_name in glob.glob(dir_name):
        if os.path.isfile(file_name):
            file_list.append(file_name)
    return file_list


def exec_cmd_in_files(cmd, dir_name):
    """
    查找目录中的文件并执行命令

    Args:
        cmd (str): 要执行的命令
        dir_name (str): 目录路径，例如 "c:/*.zip"

    Returns:
        None
    """
    files = find_files(dir_name)
    for f in files:
        os.system(cmd + "\"" + f + "\"")


def find_sub_dirs(dir_name):
    """
    查找目录中的子文件夹

    Args:
        dir_name (str): 目录路径

    Returns:
        list: 找到的子文件夹列表
    """
    dir_list = []
    for d in glob.glob(dir_name + "/*"):
        if os.path.isdir(d):
            dir_list.append(d)
    return dir_list


def get_file_list(path: str, recursive: bool):
    """
    获取给定路径下的所有文件路径，包含子目录

    Args:
        path (str): 路径
        recursive (bool): 是否递归子目录

    Returns:
        list: 包含所有文件的路径列表
    """
    file_list = []
    if not os.path.exists(path):
        return file_list
    if recursive:
        for root, dirs, files in os.walk(path):
            for i in files:
                i_path = os.path.join(root, i)
                if os.path.isfile(i_path):
                    file_list.append(i_path)
    else:
        files = os.listdir(path)
        for i in files:
            i_path = os.path.join(path, i)
            if os.path.isfile(i_path):
                file_list.append(i_path)
    return file_list
