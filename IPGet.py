#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/22 18:49
# @Author  : Zhiyue Chen
# @File    : IPGet.py
# @Description : Get local IP address
from urllib.request import urlopen


def GetIP():
    return urlopen('http://ip.42.pl/raw').read().decode()
