# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 第一步  导入第三方库
# 第二部   获取目标网页
# 第三部  解析目标网页
# 第四部 下载目标网页数据

import requests
import lxml.html
import csv


doubanUrl = 'https://movie.douban.com/top250?start={}&filter='

def getSource(url):
    #  获取网页的数据
    response = requests.get(url)
    response.encoding = 'utf-8'

    return response.content
#定义 一个函数  目的：获取每一条电影的信息
def getEveryItem(source):

    selector = lxml.html.document_fromstring(source)

    #获取每一条电影信息，并把他们放到一个集合里面
    movieItemList = selector.xpath('//div[@class="info"]')

    #定义一个列表 目的： 展示信息
    movieList=[]

    #用forxi=循环把这个电影的信息展开
    for eachMovie in movieItemList:
        #保存电影的信息 名字 地址 评分...
        #把字典里面的信息用列表展示[{movieDict1},{movieDict2}]
        movieDict ={}

        title = eachMovie.xpath('div[@class="hd"]/a/span[@class="title"]/text()')
        print(title)
        otherTitle = eachMovie.xpath('div[@class="hd"]/a/span[@class="other"]/text()')#副标题
        link =eachMovie.xpath('div[@class="hd"]/a/@href')[0]  #url
        star =eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating num"]/text()')
        quote=eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()') #引言（名句）

        #保存到字典中
        movieDict['title'] = ''.join(title+otherTitle)
        movieDict['url'] = link
        movieDict['star'] = star
        movieDict['quote'] = quote
        print(movieDict)
        movieList.append(movieDict)

        return movieList

    #第四部  下载目标网页数据
    #定义一个函数  目的：写数据
    def writeData(movieList):

        with open('./MovieDouban.csv','w',encoding='utf-8') as f:

            writer = csv.DictWriter(f,fieldnames=['title','star','quote','url'])
            writer.writeheader()

        for each in movieList:

            writer.writerow(each)

    if __name__ == '__main__':
        movieList = []
        for i in range(10):
            pageLink = doubanUrl.format(i*25)
            print(pageLink)
            movieList += getEveryItem(source)
            print(movieList[:10])
            writeData(movieList)





