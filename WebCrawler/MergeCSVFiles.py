#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 09:07
# @Author  : Zhiyue Chen
# @File    : MergeCSVFiles.py
# @Description : Merge all CSV files
import os
import pandas as pd

# change it to your folder path of collections
folderpath = r"C:\Users\czy\Desktop\Unfinished\iGEM\data\software\dataset\collections"
all_data = pd.DataFrame()
for filename in os.listdir(folderpath):
    filepath = os.path.join(folderpath, filename)
    data = pd.read_csv(filepath)
    all_data = pd.concat([all_data, data])
all_data.to_csv(os.path.join(r'C:\Users\czy\Desktop\Unfinished\iGEM\data\software\dataset', 'all_collections.csv'),
                index=None)
