#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 11:26
# @Author  : Zhiyue Chen
# @File    : Preprocessing.py
# @Description : Perform Preprocessing
import pandas as pd
import os

# Change it to the path of your data
filepath = r"C:\Users\czy\Desktop\Unfinished\iGEM\data\software\dataset\all_collections.csv"
data = pd.read_csv(filepath)
# data.using_parts.fillna('self')
for index, row in data.iterrows():
    if pd.isna(row['parts_used']) or row['parts_used'] == 'N o n e':
        data.at[index, 'parts_used'] = 'None'
    if pd.isna(row['using_parts']) or row['using_parts'] == 'N o n e':
        data.at[index, 'using_parts'] = 'self'
    if pd.isna(row['twins']) or row['twins'] == 'N o n e':
        data.at[index, 'twins'] = 'None'
data.fillna('None', inplace=True)
data.to_csv(os.path.join(r'C:\Users\czy\Desktop\Unfinished\iGEM\data\software\dataset', 'all_collections_filted.csv'),
            index=None)
