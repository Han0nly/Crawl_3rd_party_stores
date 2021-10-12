#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
-------------------------------------------------
@File    : utils.py
@Time    : 2021/10/12 4:13 下午
@Author  : Han0nly
@Github  : https://github.com/Han0nly
@Email   : zhangxh@stu.xidian.edu.cn
-------------------------------------------------
"""


def parse_installs(installs_str):
    if installs_str and installs_str.strip():
        if installs_str.endswith("万"):
            installs_int = float(installs_str[:-1]) * 10000
        elif installs_str.endswith("亿"):
            installs_int = float(installs_str[:-1]) * 100000000
        elif installs_str.endswith('万下载'):
            installs_int = float(installs_str[:-3]) * 10000
        elif installs_str.endswith('亿下载'):
            installs_int = float(installs_str[:-3]) * 100000000
        elif installs_str.endswith('万次'):
            installs_int = float(installs_str[:-2]) * 10000
        elif installs_str.endswith('次'):
            installs_int = float(installs_str[:-1])
        elif installs_str.endswith('下载'):
            installs_int = float(installs_str[:-2])
        else:
            installs_int = float(installs_str)
    else:
        installs_int = 0
    return installs_int
