# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:50:54 2019

@author: liuwp
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
import unicodedata

def get_width(s: str) -> int:
    width = len(s)
    for c in s:
        if unicodedata.east_asian_width(c) in ('W', 'F', 'A'):
            width += 1
    return width

def getHtmlText(url):
    try:
        r = requests.get(url,timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error")

def parText(result,text):
    mark = re.search(r'[0-9]\.[0-9] \(.+\)',text)
    name = re.search(r'.*\n\nRank',text)
    if name and mark:
        name = name.group().split('\n')
        name = name[0].split('/') #有些动漫会有多个名字,为了避免打印出来的信息过长,只采用第一个/前的信息
        result.append([name[0] ,mark.group()])

def printResult(result):
    tplt = '{0:<100} {1:<4}'
    print(tplt.format("\rname", "mark")) #打印表头
    for g in result:
        strlen = get_width(g[0])
        print(g[0],end="")
        for i in range(100 - strlen): #根据字符串长度对齐
            print(" ",end="")
        print(g[1])

if __name__ == '__main__':
    start_url = 'http://bangumi.tv/anime/browser?sort=rank&page='
    result = []
    depth = 100
    for count in range(1,depth+1):
        try: #如果某个页面出错则继续爬取下一页
            url = start_url + str(count)
            html = getHtmlText(url)
            soup = BeautifulSoup(html,'html.parser')
            for i in soup.find_all('div','inner'):
                parText(result,i.get_text())
            print("\r进度:{:2f}%".format(count * 100 / depth), end="") #打印进度
        except:
            print("\r进度:{:2f}%".format(count*100/depth),end="")
            continue
#    printResult(result)
    
f=open('E:/test.txt','a',encoding='utf-8')
for i in range(0,len(result)):
    s = str(result[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
##    s = s.replace("'",'').replace(',','') +'\n'   #去除单引号，逗号，每行末尾追加换行符
    s = s.replace("'",'') +'\n'
    f.write(s)
f.close()