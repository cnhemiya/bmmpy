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
from typeguard import typechecked


@typechecked
def replace_text_in_file(file_path: str, str_dict: dict[str, str], encoding="utf-8") -> None:
    """
    根据提供的字符串字典替换文件中的文本。

    Args:
        file_path (str): 要操作的文件路径。
        str_dict (dict[str, str]): 字符串字典，格式为 {"text_old1": "text_new1", "text_old2": "text_new2"}。
        encoding (str): 文件编码，默认为 "utf-8"。

    Returns:
        None
    """
    text = read_text(file_path=file_path, encoding=encoding)
    result = bmmstring.replace_string_by_dict(text=text, str_dict=str_dict)
    write_text(file=file_path, text=result, encoding=encoding)


@typechecked
def read_text(file_path: str, encoding: str = "utf-8") -> str:
    """
    读取文件的所有文本内容

    Args:
        file_path (str): 文件路径
        encoding (str): 文件编码，默认为 "utf-8"

    Returns:
        str: 文件内容

    Raises:
        FileNotFoundError: 当指定的文件不存在时抛出
        IOError: 当文件无法读取时抛出
    """
    with open(file=file_path, mode="rt", encoding=encoding) as f:
        result = f.read()
    return result


@typechecked
def write_text(file_path: str, text: str, encoding: str = "utf-8") -> None:
    """
    将文本写入文件。

    Args:
        file_path (str): 文件路径
        text (str): 要写入的文本内容
        encoding (str): 文件编码，默认为 "utf-8"

    Returns:
        None

    Examples:
        >>> write_text("example.txt", "Hello, World!")
        >>> write_text("data.txt", "Python is awesome!", encoding="gbk")
    """
    with open(file_path, "w", encoding=encoding) as file:
        file.write(text)


@typechecked
def find_files(dir_name: str) -> list[str]:
    """
    使用通配符查找目录中的文件

    Args:
        dir_name (str): 目录路径，例如 "c:/*"

    Returns:
        list: 找到的文件列表

    Examples:
        >>> find_files("test/*")
        ['test/file1.txt', 'test/file2.py']

    Note:
        该函数会递归查找所有匹配模式的文件。
    """
    # 使用 glob 模块进行通配符匹配
    # 支持如 *、?、[abc] 等通配符语法
    pattern = dir_name

    # 获取所有匹配的文件路径
    matched_files = glob.glob(pattern, recursive=True)

    # 过滤掉目录，只保留文件
    files_only = [f for f in matched_files if os.path.isfile(f)]

    return files_only


@typechecked
def exec_cmd_in_files(cmd: str, dir_name: str) -> None:
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


@typechecked
def find_sub_dirs(dir_name: str) -> list[str]:
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


@typechecked
def get_file_list(path: str, recursive: bool) -> list[str]:
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
