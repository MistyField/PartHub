#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/27 2:10
# @Author  : Zhiyue Chen
# @File    : app.py
# @Description : The body of the Flask framework
import time

from flask import Flask
from flask import render_template, request
from SearchHistory import SaveSearchHistory, DisplaySearchHistory
from SearchURLConverter import historyURL2searchURL
from NodeSearch import SearchNode, InitDatabase, MultipleSearchNode, GetSequence
from SearchTypeConverter import SearchTypeConvert
from Paginator import GetPage, GetPageNum
from NodeSort import SortNode
from IPGet import GetIP

app = Flask(__name__)
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
ip = GetIP()
try:
  stop = open(r'stopwords.txt', 'r+', encoding='utf-8')
  stopword = stop.read().split("\n")
except:
  stopword = []


@app.route('/')
def index():  # put application's code here
    index_isvalid = True
    return render_template('Search.html', flag=index_isvalid)


@app.route('/sp', methods=['GET', 'POST'])
def search():
    global type
    global key
    p = request.args.get("p", '')
    show_homepage_status = 0  # 1 means show
    if p == '':
        p = 1
    else:
        p = int(p)
    key = request.args.get('s')
    type = request.args.get('searchtype')
    sort = request.args.get('sort', '')
    if sort == '':
        sort = 'default'
    if not key or not type:
        index_isvalid = False
        return render_template('Search.html', flag=index_isvalid, key=key, type=type)
    else:
        if type == 'sequence':
            for single_w in key:
                if single_w not in ['a','t','g','c','A','T','G','C']:
                    return 'Please enter the sequence...'
        SaveSearchHistory({key: type})
        if ' AND ' in key:
            kwd_list = key.split(' AND ')
            multiple_type = 'AND'
            for single_kwd in kwd_list:
                if single_kwd in stopword:
                    return 'Please enter a legal search term'
            all_res = MultipleSearchNode(kwd_list, type, 'AND')
        elif ' OR ' in key:
            kwd_list = key.split(' OR ')
            multiple_type = 'OR'
            for single_kwd in kwd_list:
                if single_kwd in stopword:
                    return 'Please enter a legal search term'
            all_res = MultipleSearchNode(kwd_list, type, 'OR')
        else:
            multiple_type = 'none'
            if key in stopword:
                return 'Please enter a legal search term'
            all_res = SearchNode(key, type)
        if all_res:
            sorted_res = SortNode(all_res, sort)
            search_res = GetPage(sorted_res, p, per_page=15)
            total, page_range = GetPageNum(sorted_res, p, per_page=15)
            if 1 in page_range:
                show_homepage_status = 1
            return render_template('SearchResult.html', key=key, type=type, res=search_res, length=len(all_res),
                                   total=total, status=show_homepage_status, p=int(p), rg=page_range, sorttype=sort,
                                   multiple_type=multiple_type)
        else:
            return 'No Search Result...'


@app.route('/sh')
def sHistory():
    res = DisplaySearchHistory()
    if res:
        for search_dic in res:
            for k, v in search_dic.items():
                url = historyURL2searchURL(k, v)
                search_dic[k] = [SearchTypeConvert(v), url]
        return render_template('SearchHistory.html', res_lst=res)
    else:
        return 'No search History...'


@app.route('/g/<part_num>/')
def fpTree(part_num):
    return render_template('Map.html', part_num=part_num, ip=ip)


@app.route('/seq/<part_num>/')
def seq(part_num):
    part_seq = GetSequence(part_num)
    return render_template('Sequence.html', part_num=part_num,seq = part_seq)


if __name__ == '__main__':
    InitDatabase()
    app.run(host='0.0.0.0', port=5000)
