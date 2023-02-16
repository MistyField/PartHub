#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/30 1:30
# @Author  : Zhiyue Chen
# @File    : Paginator.py
# @Description : Pagination of search results
import math


def GetPageNum(lst, p, per_page):
    total = int(math.ceil(len(lst) / per_page))
    show_page = 5  # Number of page numbers displayed
    pageoffset = 2  # Display offset
    start = 1  # Start of pagination bar
    end = total  # End of pagination bar
    if total > show_page:
        if p > pageoffset:
            start = p - pageoffset
            if total > p + pageoffset:
                end = p + pageoffset
            else:
                end = total
        else:
            start = 1
            if total > show_page:
                end = show_page
            else:
                end = total
    else:
        if p + pageoffset > total:
            start = start - (p + pageoffset - end)
    return total, range(start, end + 1)


def GetPage(lst, p, per_page):
    if p == 1:
        return lst[0:per_page]
    else:
        return lst[(int(p) - 1) * per_page:int(p) * per_page]
