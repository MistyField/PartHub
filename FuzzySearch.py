#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 0:02
# @Author  : Zhiyue Chen
# @File    : FuzzySearch.py
# @Description : Perform fuzzy searches to make the search results more comprehensive
from multiprocessing.dummy import Pool as ThreadPool
import re
from fuzzywuzzy import fuzz


def FuzzyMatch(key, nodes):
    """

    Args:
        key: String for search key
        nodes: List containing all nodes

    Returns: List containing more than the fuzzy search threshold

    """

    def FuzzyMatchOne(item):
        """
        To perform fuzzy judgment for a single node to determine if the semantic relevance exceeds a threshold
        Args:
            item: A list like [key, node]

        Returns: A tuple like ("match", i, distance_score, 1)

        """
        _key = item[0]
        node = item[1]
        i = item[2]
        temp = dict(node).get('description').lower()
        if _key in temp:
            res.append(("match", i, 200, 1))
        try:
            match_score = fuzz.partial_ratio(_key, temp)
        except:
            match_score = 0
        # The matching value is too low, it will be rejected directly
        if match_score < 120:
            return
        else:
            distance_score = SearchNearest(_key, temp)
            res.append(("match", i, distance_score, 1))

    res = []
    output = []
    pool = ThreadPool()
    items = [[key, node, i] for i, node in enumerate(nodes)]
    pool.map_async(FuzzyMatchOne, items)
    pool.close()
    pool.join()
    res = list(set(res))
    if len(res) >= 15:
        for item in res:
            out_ind = item[1]
            out_node = dict(nodes[out_ind])
            if len(out_node['contents']) > 200:
                out_node['matched_contents'] = out_node['contents'][:200]
            out_node['fuzzy_ratio'] = item[2]
            output.append(out_node)
    return output


def SearchNearest(key, doc):
    """

    Args:
        key: String for search key
        doc: Part contents

    Returns: Distance_score

    """
    key_list = key.split(" ")
    distance_score = 0
    word_loc = []
    for word in key_list:
        # Save the position of the word in the tex
        temp = [m.start() for m in re.finditer(word, doc)]
        word_loc.append(temp)
    for ind in range(len(word_loc) - 1):
        distance_score += CalculateDistance(word_loc[ind], word_loc[ind + 1])
    return distance_score


def CalculateDistance(a, b):
    def cal(x):
        return min([abs(i - x) for i in b])

    return min([cal(x) for x in a])


def CalculateFuzzyRatio(key, node_dic):
    temp = node_dic.get('description').lower()
    if key in temp:
        node_dic['fuzzy_ratio'] = 200
    else:
        node_dic['fuzzy_ratio'] = fuzz.partial_ratio(key, temp)
