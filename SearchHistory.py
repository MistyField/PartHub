#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/5 0:01
# @Author  : Zhiyue Chen
# @File    : SearchHistory.py
# @Description : Save and display search history
import json


def SaveSearchHistory(search_dic):
    filename = "SearchHistory.json"
    with open(filename, 'r') as file_obj:
        try:
            content = json.load(file_obj)
            content.update(search_dic)
            with open(filename, 'w') as f_new:
                json.dump(content, f_new)
        except:
            with open(filename, 'w') as f_new:
                json.dump(search_dic, f_new)
            pass


def DisplaySearchHistory():
    filename = "SearchHistory.json"
    res = []
    with open(filename, 'r') as file_obj:
        try:
            content = json.load(file_obj)
            length = len(content.items())
            index = 0
            for search in content.items():
                if length - index < 100:
                    res.append({search[0]:search[1]})
                index += 1
        except:
            pass
        return res[::-1]
