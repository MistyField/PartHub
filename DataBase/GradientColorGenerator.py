#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/17 16:16
# @Author  : Zhiyue Chen
# @File    : GradientColorGenerator.py
# @Description : Generate gradient color according to the time of the part
from datetime import datetime

# RGB value of the standard color
green = [89, 131, 100]
orange = [238, 153, 77]
begin_time = datetime.strptime('2004-1-1', '%Y-%m-%d')


def GradientColorGenerate(time):
    try:
        exact_time = datetime.strptime(time, '%Y-%m-%d')
    except:
        exact_time = datetime.strptime('2004-1-1', '%Y-%m-%d')
    now = datetime.now()
    max_interavl = now - begin_time
    max_range = max_interavl.days
    interval = now - exact_time
    interval_days = interval.days
    rgb_color = [round(green[i] + (orange[i] - green[i]) * interval_days / max_range) for i in range(3)]
    res = r'#'
    for val in rgb_color:
        res = res + str(hex(val))[2:].upper()
    return res
