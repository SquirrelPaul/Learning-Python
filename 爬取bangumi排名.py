
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
#import re
import unicodedata
import pandas as pd

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
    name_search = text.find("a", class_='l')
    if name_search:
        name = name_search.get_text()
        rank = text.find("span", class_='rank').get_text()[5:]    #去除 rank四个字符，只留下数字
        mark = text.find("small", class_='fade').get_text()
        count = text.find("span", class_='tip_j').get_text()[1:-4]  #去除括号以及 人评分 这些字符，只留下数字
        info = text.find("p",class_='info tip').get_text().strip()    #番剧的具体信息，会降低爬取速度，不需要时可以去掉
        result.append((name, rank, mark, count, info))
##根据名称对齐的函数，暂时用不到
#def printResult(result):
#    tplt = '{0:<100} {1:<4}'
#    print(tplt.format("\rname", "mark")) #打印表头
#    for g in result:
#        strlen = get_width(g[0])
#        print(g[0],end="")
#        for i in range(100 - strlen): #根据字符串长度对齐
#            print(" ",end="")
#        print(g[1])
if __name__ == '__main__':
    start_url = 'http://bangumi.tv/anime/browser?sort=rank&page='  #【爬取网页指定】 可根据类型、时间、标签筛选出来的新URL进行筛选，统一加上&page=,作为start_url
    result = []
    depth = 224
    for count in range(1,depth+1):
        try: #如果某个页面出错则继续爬取下一页
            url = start_url + str(count)
            html = getHtmlText(url)
            soup = BeautifulSoup(html,'html.parser')
            for i in soup.find_all('div','inner'):
                parText(result, i)
            print("\r进度:{:2f}%".format(count * 100 / depth), end="") #打印进度
        except Exception as e:
            print("\r进度:{:2f}%".format(count*100/depth),end="")
            print()
            print(str(e))
            continue
pd.DataFrame(result, columns=['番剧名称', 'Bangumi排名', '评分', '评分人数','番剧信息']).to_csv('E:/test.txt', index=None, encoding='utf-8',sep='-')  # 【指定字段写入的规则】以sep的属性作为分隔符，将文件写入txt文件中