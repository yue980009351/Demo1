# -*- coding: utf-8 -*-
import urllib
from pandas import *
import re
import os
import matplotlib.pyplot as plt
from pylab import *
import random
import string

def main():
    # 指定默认字体
    mpl.rcParams['font.sans-serif'] = ['SimHei']

    #获取平均分
    def pf(FilmId):
        pjf = 0
        sum = 0
        pf_url = 'http://movie.mtime.com/' + FilmId + '/'
        pf_req = urllib.request.Request(pf_url, headers={'User-Agent': 'Magic-Browser'})
        pf_str1 = urllib.request.urlopen(pf_req)
        pf_str2 = pf_str1.read().decode("utf-8")
        pf_str3 = re.findall(r'<span class="db_point ml6">+.+</span>', pf_str2)
        if len(pf_str3) == 0:
            return pjf
        for t in pf_str3:
            pf_str4 = re.findall(r'(?<=<span class="db_point ml6">)(.*?)(?=</span>)', t)
            sum = sum + float(pf_str4[0])
        pjf = sum/len(pf_str3)
        return pjf

    #获取电影类型
    def lx(FilmId):
        lx_url = 'http://movie.mtime.com/' + FilmId + '/'
        lx_req = urllib.request.Request(lx_url, headers={'User-Agent': 'Magic-Browes'})
        lx_str1 = urllib.request.urlopen(lx_req)
        lx_str2 = lx_str1.read().decode("utf-8")
        lx_str3 = re.findall(r'<div class="otherbox __r_c_" pan="M14_Movie_Overview_MovieTypeAndRuntimeAndVersion">+.+</div>', lx_str2)
        for t in lx_str3:
            lx_str4 = re.findall(r'(?<=target="_blank" property="v:genre">)(.*?)(?=</a>)',t)
            return lx_str4

    #数据抓取
    url = 'http://theater.mtime.com/China_Beijing/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Magic-Browser'})
    str1 = urllib.request.urlopen(req)
    str2 = str1.read().decode("utf-8")
    start = str2.find('hotplaySvList = [')
    if start == -1:
        os.exit()
    str3 = str2[start:-1]
    end = str3.find(';')
    if end == -1:
        os.exit()
    str3 = str3[len(' hotplaySvList = ['):end]
    str4 = str3.split('},{')
    dict1 = {}
    dict2 = {}
    list_film = []
    list_id = []
    list_pf = []
    list_lx = []
    for t1 in str4:
        f1_str1 = t1.split(',')
        id = f1_str1[0].split(':')[-1].strip()
        film = f1_str1[-1].split('"')[-2].strip()
        dict1[id] = film
        list_id.append(id)
        list_film.append(film)
        score = pf(id)
        list_pf.append(score)
        list_lx.append(lx(id))

    dict2['影视ID'] = list_id
    dict2['影视名称'] = list_film
    dict2['影视评分'] = list_pf
    dict2['影视类型'] = list_lx
    df = DataFrame(dict2)
    df0 = df.sort_values(by='影视评分', ascending=False)
    df0.index = range(0, len(df0))
    print('--------------------------数据1----------------------------')
    print(df0[:20])
    print('-----------------------------------------------------------')

    #数据抓取
    list2_url = ['http://www.mtime.com/top/movie/top100/', 'http://www.mtime.com/top/movie/top100/index-2.html']
    frames = []
    for str_url in list2_url:
        url02 = str_url
        req02 = urllib.request.Request(url02, headers={'User-Agent': 'Magic-Browser'})
        str01 = urllib.request.urlopen(req02)
        str02 = str01.read().decode("utf-8")
        str03 = re.findall(r'(?<=<ul id="asyncRatingRegion">)(.*?)(?=</ul></div><div id="PageNavigator")+', str02)
        dict01 = {}
        dict02 = {}
        list2_id = []
        list2_name = []
        list2_lx = []
        list2_pf = []
        for t01 in str03:
            str04 = re.findall(r'(?<=<div class="mov_con">	<h2 class="px14 pb6"><a)(.*?)(?=</h2>)', t01)
            for t02 in str04:
                list2_id.append(re.findall(r'(?<=href="http://movie.mtime.com/)(.*?)(?=/" target="_blank">)', t02)[0])
                list2_name.append(re.findall(r'(?<=" target="_blank">)(.*?)(?=&nbsp;)', t02)[0])
            list2_lx_temp = re.findall(r'(?<=<p>类型：<span)(.*?)(?=</span></p>)', t01)
            for t03 in list2_lx_temp:
                list2_lx.append(re.findall(r'(?<=" target="_blank">)(.*?)(?=</a>)', t03))
            list2_pf_temp = re.findall(r'(?<=<b class="point" ><span class=total>)(.*?)(?=</span></b>)', t01)
            for t4 in list2_pf_temp:
                iteml2 = re.findall(r'(\d+\.?\d*)', t4)
                list2_pf.append(float(iteml2[0] + '.' + iteml2[-1]))
        dict01['影视ID'] = list2_id
        dict01['影视名称'] = list2_name
        dict01['影视评分'] = list2_pf
        dict01['影视类型'] = list2_lx
        df01 = DataFrame(dict01)
        frames.append(df01)
    #整合数据
    result = pandas.concat(frames)
    result.index = range(0, len(result))
    print('--------------------------数据2----------------------------')
    print(result)
    print('-----------------------------------------------------------')

    #整合两个数据源所获取的数据
    list_frames = [df0[:20], result]
    df_result = pandas.concat(list_frames)
    df_result.index = range(0, len(df_result))
    print('------------------------数据整合---------------------------')
    print(df_result)
    print('-----------------------------------------------------------')

    del df_result['影视ID']
    del df_result['影视名称']

    #显示各类型评分数据
    list_dylx = []
    list_dypf = []
    df2 = DataFrame({'影片类型': [], '电影评分': []})
    for i in range(len(df_result['影视类型'])):
        for j in range(len(df_result['影视类型'][i])):
            list_dylx.append(df_result['影视类型'][i][j])
            list_dypf.append(df_result['影视评分'][i])

    df2['影片类型'] = list_dylx
    df2['电影评分'] = list_dypf
    df3 = df2.groupby(by=df2['影片类型'], as_index=False).mean().sort_values(by='电影评分', ascending=False)
    df3.index = range(1, len(df3)+1)
    print('-------------------电影类型评分统计列表--------------------')
    print(df3[0:20])
    print('-----------------------------------------------------------')

    #产生随机颜色
    color = []
    str = ""
    for cl in df3[:20].index:
        color.append('#' + str.join(
            random.sample(['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 6)).replace(
            " ", ""))

    #将统计结果图形化展现
    figure(1, figsize = (8, 6))
    plt.ylabel('影视评分')
    plt.xlabel('影视类型')
    plt.title('影视类型评分分析图')
    tu = plt.bar(left=df3[0:20].index, height=df3[0:20]['电影评分'],
                 color=color, width=0.9, align="center", yerr=0.00001)
    label = []
    for lb in df3[0:20]['影片类型']:
        label.append(lb)
    plt.xticks(df3[0:20].index, label)
    plt.legend(tu, label)
    plt.show()

if __name__ == "__main__":
    main()
