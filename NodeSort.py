#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/4 23:56
# @Author  : Zhiyue Chen
# @File    : NodeSort.py
# @Description : Sort nodes according to different fields
from operator import itemgetter
from datetime import datetime


def SortNode(node_dic_lst, sorttype):
    if sorttype == 'cite':
        return sorted(node_dic_lst, key=lambda x: int(x['cites']), reverse=True)
    elif sorttype == 'match':
        return sorted(node_dic_lst, key=itemgetter('fuzzy_ratio'), reverse=True)
    elif sorttype == 'recent':
        return RecentSort(node_dic_lst)
    elif sorttype == 'default':
        return DefaultSort(node_dic_lst)


def DefaultSort(node_dic_lst):
    now = datetime.now()
    for node in node_dic_lst:
        try:
            interval = now - datetime.strptime(node['date'], '%Y-%m-%d')
        except:
            interval = now - datetime.strptime('2004-1-1', '%Y-%m-%d')
        sample_score = 0
        released_score = 0
        favorite_score = 0
        if node['sample'] == 'Sample In stock':
            sample_score = 20
        if node['released'] != 'Not Released':
            released_score = 20
        if node['isfavorite'] != 'False':
            favorite_score = 10
        node['score'] = int(node['twins_num']) * 5 + int(node['citing']) * 5 + int(
            node['cites']) * 5 - interval.days / 219 + sample_score + released_score + favorite_score
    return sorted(node_dic_lst, key=itemgetter('score'), reverse=True)


def RecentSort(node_dic_lst):
    for node in node_dic_lst:
        try:
            node['score'] = datetime.strptime(node['date'], '%Y-%m-%d')
        except:
            node['score'] = datetime.strptime('2004-1-1', '%Y-%m-%d')
    return sorted(node_dic_lst, key=itemgetter('score'), reverse=True)
