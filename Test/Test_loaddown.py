from bs4 import BeautifulSoup
import requests
import re

class downloader(object):

    def __init__(self):
        self.server='http://www.jjwxc.net/'
        self.target='http://www.jjwxc.net/onebook.php?novelid=2443908'
        self.names=[]       #章节名
        self.urls=[]        #章节链接
        self.nums=0         #章节数

    def get_download_url(self):
        req=requests.get(url=self.target)
        req.encoding='gb2312'       #显示指定网页编码
        html=req.text
        table_bf=BeautifulSoup(html,'lxml')
        table=table_bf.find_all('table',class_='cytable')
        tr_bf=BeautifulSoup(str(table[0]),'lxml')
        a=tr_bf.find_all('a', itemprop='url')
        self.nums=len(a)  # 剔除不必要的章节，并统计章节数
        for each in a:
            self.names.append(each.string)
            self.urls.append(each.get('href'))

    def get_contents(self,target):
        req=requests.get(url=target)
        req.encoding='gb2312'
        html=req.text
        bf=BeautifulSoup(html,'lxml')
        names=bf.find_all('div',style='float:left;width:713px;padding-left: 0px; padding-top:14px;font-size:16px;')
        #print(names[0].string)      #章节名

        addcomments=bf.find_all('div',class_='readsmall')   #避免最后有“作者有话要说”

        contents=bf.find_all('div',class_='noveltext')

        contentstr=str(contents[0])

        if addcomments:
            addcommentstr = str(addcomments[0])
            contentstr=contentstr.replace(addcommentstr,'')            #删去最后的附言

        pattern=re.compile('.*?<br/>')                      #选出所有以<br/>为结尾的
        conts=re.findall(pattern,contentstr)


        conts[0]=conts[0].lstrip()

        for i in range(len(conts)):
            conts[i]=conts[i].replace('&lt;br/&gt;','')            #去掉&lt;br/&gt;

        return conts

    def writer(self,name,path,text):
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.writelines(text)
            f.write('\n\n')

if __name__=='__main__':
    dl=downloader()
    dl.get_download_url()
    dl.get_contents(dl.urls[0])
    print('开始下载!')
    for i in range(dl.nums):
        dl.writer(dl.names[i],'陆花1.txt',dl.get_contents(dl.urls[i]))
        #stdout.write('已下载：%.3f%%' % float(i/dl.nums)+'\r')
        #stdout.flush()
        print('\r','已下载：  %.3f%%' % float(i/dl.nums*100),end='',flush=True)
    print('\r', '已下载：  100%',end='',flush=True)
    print('\n下载完成!')