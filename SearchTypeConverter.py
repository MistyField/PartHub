#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 15:57
# @Author  : Zhiyue Chen
# @File    : SearchTypeConverter.py
# @Description : Convert search type from neo4j to web display
def SearchTypeConvert(type):
    """
    To convert search type from neo4j to web display
    """
    neo4j2web_dic = {'number': 'ID', 'name': 'Name', 'sequence': 'Sequence', 'designer': 'Designer',
                     'team': 'Team', 'contents': 'Content'}
    if type not in neo4j2web_dic:
        return
    else:
        return neo4j2web_dic[type]
