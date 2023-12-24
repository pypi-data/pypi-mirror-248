#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: 文件.py
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关 文件 的自动化操作
#############################################
import os


def count_line(code_path: str, suffix: str = '.py') -> list:
    """
    统计代码行数
    :param code_path: 代码位置
    :param suffix: 代码后缀。TODO：未来增加更多代码格式
    :return: list：总行数、空行数、注释行数
    """
    file_list = [os.path.join(root, file) for root, dirs, files in os.walk(code_path) for file in files if
                 file.endswith(suffix)]
    count_of_code_lines = 0
    count_of_blank_lines = 0
    count_of_annotation_lines = 0
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as fp:
            content_list = fp.readlines()
            for content in content_list:
                content = content.strip()
                if content == '':
                    count_of_blank_lines += 1
                elif content.startswith('#'):
                    count_of_annotation_lines += 1
                else:
                    count_of_code_lines += 1
    return [count_of_code_lines, count_of_blank_lines, count_of_annotation_lines]


def api():
    print(666)
