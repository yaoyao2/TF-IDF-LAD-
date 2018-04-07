#!/usr/bin/python
# -*- coding:utf8 -*-

import  urllib.request
from bs4 import BeautifulSoup
import re

nameList=[]
Names=[]

def namePaChong(yearBeg,yearEnd):
    global nameList
    global Names
    f = open('name.txt','w',encoding='utf-8')
    for year in range(yearBeg,yearEnd):
        print(year)
        url = r'https://baike.baidu.com/item/'+str(year)+'%E5%B9%B4'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')

        # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
        soup = BeautifulSoup(html, 'html.parser')

        # name = soup.find_all('div', 'para')  # 查找所有div标签中class='para'的语句
        name = soup.find_all('a', target='_blank')  # 查找所有div标签中target='_blank'的语句
        for n in name:
            s = n.string
            nameList.append(str(s))
            # print(s)

    Names=list(set(nameList))

    for n in Names:
        f.write(n + '\n')

    f.close()



def findPolyName(nameF):
    fs=open('polyName.txt','w')
    count=0
    with open(nameF,encoding='utf8') as f:
        line=f.readline().strip('\n')
        while line:
            count=count+1
            if(count>827):
                hanzi = urllib.parse.quote(line)
                url = r'https://baike.baidu.com/item/' + hanzi
                res = urllib.request.urlopen(url)
                html = res.read().decode('utf-8')

                # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
                soup = BeautifulSoup(html, 'html.parser')
                polyTxt = soup.find_all('div', 'polysemantList-header-title')  # 查找所有span标签中class='sorryTxt'的语句
                if (polyTxt):
                    string = str(polyTxt[0])
                    beg = string.find('<b>')
                    end = string.find('</b>')
                    print(string[beg + 3:end])
                    fs.write(string[beg + 3:end]+'\n')
                    # print("可以找到" + line)
                else:
                    # print ("抱歉，找不到" + line)
                    pass
            line = f.readline().strip('\n')
    f.close()


def findLink(path):
    fs=open('nameLink.txt','w',encoding='utf-8')
    count=0
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            hanzi = urllib.parse.quote(line)
            url = r'https://baike.baidu.com/item/' + hanzi+'?force=1'
            res = urllib.request.urlopen(url)
            html = res.read().decode('utf-8')

            # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup)
            text=soup.find_all(href=re.compile("/item/%"))
            for t in text:
                count = count + 1
                string=str(t)
                beg=string.find('href="')
                end=string.find('" target=')

                print(str(count)+' '+line+' '+string[beg+6:end])
                fs.write(str(count)+' '+line+' '+string[beg+6:end]+'\n')

            line=f.readline().strip('\n')
    fs.close()
    pass


def findInfoBox(path):
    fs = open('nameInfoBox.txt', 'w', encoding='utf-8')
    with open(path, encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            line=line.split(' ')
            url = r'https://baike.baidu.com'+line[2]
            print(url)
            res = urllib.request.urlopen(url)
            html = res.read().decode('utf-8')
            # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup)

            names = soup.find_all('dt','basicInfo-item name')
            values = soup.find_all('dd','basicInfo-item value')

            for i in range(len(names)):
                print (i)
                rel=str(names[i].get_text()).strip('\n')
                val=str(values[i].get_text()).strip('\n')
                Line=line[0] + ' '+ line[1] +' ' + rel + ' ' + val
                if(val=='None'):
                    print(Line)
                fs.write(Line+'\n')

            line = f.readline().strip('\n')
    fs.close()
    pass

def findRelNum(path):
    fs=open('nameRel.txt','w',encoding='utf-8')
    relList=[]
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip('\n')

        while line:
            line=line.split(' ')
            relList.append(line[2])

            line=f.readline().strip('\n')

    rel=list(set(relList))

    for r in rel:
        print(len(rel))
        print(r)
        fs.write(r+'\n')

    pass




if __name__=='__main__':
    yearBeg=1987
    yearEnd=1999
    namePaChong(1987,1988)#生成name.txt文件

    findPolyName('name.txt')#生成polyName.txt文件

    findLink('polyname.txt')#生成nameLink.txt文件

    findInfoBox('nameLink.txt')#生成nameInfoBox.txt文件

    findRelNum('nameInfoBox.txt')#生成nameRel.txt文件
    pass




