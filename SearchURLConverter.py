#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 15:35
# @Author  : Zhiyue Chen
# @File    : SearchURLConverter.py
# @Description : Convert keyword and type to search URL
import re


def historyURL2searchURL(k, v):
    raw_url = '/sp?s=key&searchtype=Type'
    temp1 = re.sub('key', k, raw_url)
    searchURL = re.sub('Type', v, temp1)
    return searchURL
