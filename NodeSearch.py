#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 18:23
# @Author  : Zhiyue Chen
# @File    : NodeSearch.py
# @Description : Search for nodes based on keywords and type
from py2neo import Node, Relationship, Graph, NodeMatcher
import re
from FuzzySearch import CalculateFuzzyRatio, FuzzyMatch

graph = Graph('http://localhost:7474/', auth=('neo4j', 'igem2022'))

node_matcher = NodeMatcher(graph)


def SearchNode(key, type):
    node_dic_list = []
    if type == 'sequence':
        key_set = set([i.lower() for i in key])
        if len(key_set.difference({"a", "t", "c", "g"})) == 0:
            key_inverse = key.replace("a", "t").replace("t", "a").replace("c", "g").replace("g", "c")
            sequence_query = "_.sequence =~ '(?i).*key.*' OR _.sequence =~ '(?i).*inverse.*'"
            sequence_query_temp = re.sub('key', key.lower(), sequence_query)
            sequence_query = re.sub('inverse', key_inverse, sequence_query_temp)
            nodes = list(node_matcher.match("Part").where(sequence_query))
        else:
            return []
    else:
        query = "_.type =~ '(?i).*key.*'"
        query_temp = re.sub('type', type, query)
        query = re.sub('key', key, query_temp)
        nodes = list(node_matcher.match("Part").where(query))
        if not nodes:
            return []
        if type in ['contents', 'name']:
            if len(nodes) < 20:
                node_dic_list = FuzzyMatch(key, all_lst)
                nums = [node['number'] for node in node_dic_list]
            else:
                nums = []
    for node in nodes:
        if type == 'contents':
            node_dic = dict(node)
            if node_dic['number'] not in nums:
                node_dic['matched_contents'] = ContentMatch(node, key)
                CalculateFuzzyRatio(key, node_dic)
                node_dic_list.append(node_dic)
        elif type == 'name':
            node_dic = dict(node)
            if node_dic['number'] not in nums:
                node_dic['matched_contents'] = dict(node)['contents'][:200]
                CalculateFuzzyRatio(key, node_dic)
                node_dic_list.append(node_dic)
        else:
            node_dic = dict(node)
            node_dic['matched_contents'] = dict(node)['contents'][:200]
            CalculateFuzzyRatio(key, node_dic)
            node_dic_list.append(node_dic)
    return node_dic_list


def ContentMatch(node, key):
    content = dict(node)['contents']
    content_lst = re.split(' ', content)
    for i in range(len(content_lst)):
        if key in content_lst[i]:
            r = 20
            if i >= r and i + r < len(content_lst) - 1:
                return ' '.join(content_lst[i - r:i + r])
            elif i >= r and i + r > len(content_lst) - 1:
                return ' '.join(content_lst[i - r:len(content_lst) - 1])
            elif i < r and i + r < len(content_lst) - 1:
                return ' '.join(content_lst[0:i + r])
            else:
                return ' '.join(content_lst[0:len(content_lst) - 1])


def InitDatabase():
    global all_lst
    all_lst = list(graph.nodes.match())
    print(' * Database initialization completed')


def MultipleSearchNode(kwd_list, type, flag):
    res = []
    if len(kwd_list) < 2:
        return
    if flag == 'AND':
        res = SearchNode(kwd_list[0], type)
        num_list = GetNumList(res)
        for kwd in kwd_list[1:]:
            if res:
                res = [i for i in SearchNode(kwd, type) if i.get('number') in num_list]
                num_list = GetNumList(res)
            else:
                return
    else:
        num_list = []
        for kwd in kwd_list:
            res = res + [i for i in SearchNode(kwd, type) if i.get('number') not in num_list]
            num_list = GetNumList(res)
    return res


def GetNumList(node_dic_list):
    return [i.get('number') for i in node_dic_list]


def GetSequence(part_id):
    raw_query = "_.number='part_id'"
    query = re.sub('part_id', part_id, raw_query)
    try:
        node = node_matcher.match('Part').where(query).first()
    except:
        return 'No sequence found...'
    return dict(node)['sequence']
