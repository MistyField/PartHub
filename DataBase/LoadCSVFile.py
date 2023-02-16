#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 13:45
# @Author  : Zhiyue Chen
# @File    : LoadCSVFile.py
# @Description : Read CSV file and import data into neo4j database
from pandas import read_csv
from py2neo import Node, Relationship, Graph, Subgraph
from tqdm import tqdm
import re
from GradientColorGenerator import GradientColorGenerate

graph = Graph('http://localhost:7474/', auth=('neo4j', 'igem2022'))

# change it to your path of all_collections_filted.csv
filepath = r"DataBase/all_collections_filted.csv"

graph.delete_all()
part_node_dict = {}
part_list = []
relationship_list = []

data = read_csv(filepath)
for i in tqdm(data.index):
    part_num = data['part_num'].values[i]
    part_name = data['part_name'].values[i]
    part_url = data['part_url'].values[i]
    part_desc = data['short_desc'].values[i]
    part_type = data['part_type'].values[i]
    part_team = data['team'].values[i]
    part_sequence = data['sequence'].values[i]
    part_contents = re.sub(' Sequence and Features', '', data['contents'].values[i])
    part_released = data['released'].values[i]
    part_sample = data['sample'].values[i]
    part_twins = data['twins'].values[i]
    part_assemble = data['assemble_std'].values[i]
    part_used = str(data['parts_used'].values[i])
    part_using = str(data['using_parts'].values[i])
    part_len = data['len'].values[i]
    part_date = data['date'].values[i]
    part_isfavorite = data['isfavorite'].values[i]
    part_year = str(data['year'].values[i])
    part_designer = data['designer'].values[i]
    try:
        part_used_list = part_used.split(' ')
        part_using_list = part_using.split(' ')
        part_twins_list = part_twins.split(' ')
        if part_used == 'None' or part_used == '' or part_used == 'N o n e':
            part_used_list = []
        if part_using == 'self' or part_using == '':
            part_using_list = []
        if part_twins == 'None' or part_twins == '' or part_twins == 'N o n e':
            part_twins_list = []
    except:
        part_used_list = []
        part_using_list = []
        part_twins_list = []
    part_node = Node('Part', number=str(part_num), name=part_name, url=part_url, description=part_desc, type=part_type,
                     team=part_team, sequence=part_sequence, contents=part_contents, released=part_released,
                     sample=part_sample, assemble=part_assemble, length=part_len, date=part_date,
                     isfavorite=str(part_isfavorite), twins=part_twins_list, twins_num=str(len(part_twins_list)),
                     cited_by=part_used_list, year=part_year, cites=str(len(part_used_list)), ref=part_using_list,
                     citing=str(len(part_using_list)), designer=part_designer, node_size=len(part_used_list) * 2 + 10,
                     color=GradientColorGenerate(part_date))
    part_list.append(part_node)
    part_node_dict.update({str(part_num): part_node})

for pNode in tqdm(part_node_dict.values()):
    if pNode['ref']:
        for ref_part in pNode['ref']:
            try:
                pNode1 = part_node_dict[ref_part]
                relationShip = Relationship(pNode, 'cite', pNode1)
                relationship_list.append(relationShip)
            except:
                pass
    if pNode['twins']:
        for twin_part in pNode['twins']:
            try:
                pNode2 = part_node_dict[twin_part]
                if pNode2['number'] != pNode['number']:
                    relationShip = Relationship(pNode, 'twins', pNode2)
                    relationship_list.append(relationShip)
            except:
                pass
    if pNode['cited_by']:
        for cite_part in pNode['cited_by']:
            try:
                pNode3 = part_node_dict[cite_part]
                relationShip = Relationship(pNode, 'cited by', pNode3)
                relationship_list.append(relationShip)
            except:
                pass
subgraph = Subgraph(part_list, relationship_list)
tx = graph.begin()
tx.create(subgraph)
graph.commit(tx)
