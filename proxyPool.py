#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/10 10:18
# @Author  : Yu
# @Site    : 
# @File    : proxy.py
import requests
from bs4 import BeautifulSoup
import subprocess as sp
from lxml import etree,html
import requests
import random
import re
from pyquery import PyQuery
import subprocess.Popen as sp
#只要获取首页 解析网页并返回IP列表
def getIp():
    url='http://www.xicidaili.com/'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.xicidaili.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',}
    try:
        r=requests.get(url,headers=header)
        r.encoding=r.apparent_encoding
        if r.status_code==200:
            print(r.status_code)
    except:
        print("link is error")
    # 可以首先用lxml的etree处理一下代码，这样如果你的HTML代码出现一些不完整或者疏漏，都会自动转化为完整清晰结构的 HTML代码
    doc=PyQuery(html.fromstring(r.text))
    tr=doc('tr')
    print(tr.length)
    #用于存储ip地址的列表
    ip_list=[]
    #遍历所有tr标签下的所有td标签的text
    for tr in tr.items():
        for td in tr.items():
            try:
                line=td.text()
            except:
                print('error')
                continue
            lis=line.split(' ')
            #判断存在并合成标准ip格式 ip+port
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',lis[0]):
                smallList=[]
                #类型
                smallList.append(lis[4])
                #ip
                smallList.append(lis[0])
                #port
                smallList.append(lis[1])
                ip_list.append(smallList)
    return ip_list
#检查代理IP的连通性
def testConnect(list):
    #定义一个连通的ip的列表
    yes_list=[]

    ##命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
    cmd='ping -n 3 -w 3 %s'
    # list是一个包含列表的列表 每个小列表0是type（http or https） 1是ip 2是port
    for IP in list:
        ip=IP[1]
        #测试IP 执行命令
        p=sp.Popen(cmd%ip,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
        #得到返回结果并解码 字符串类型
        out=p.stdout.read().decode('gbk')
        print(out)
        #正则获取丢包数目
        try:
            Lost_packet = re.search(r'丢失 = \d{1,4}', out).group().split(' ')[-1]
            # 正则获取Ping的平均时间
            average_time = re.search(r'平均 = \d{1,4}ms', out).group().split(' ')[-1][:-2]
        except:
            print('匹配不到，默认全部丢失,继续下一个IP测试')
            continue
        if int(Lost_packet)>=2:
            print('丢包现象较多，此IP作废，继续下一个IP测试')
            continue
        elif int(average_time)>=1000:
            print("平均耗时过长，此IP作废，继续下一个IP测试")
            continue
        else:
            #有效IP 类型 端口ip地址存入有用列表
            yes_list.append(IP)
    #返回有效IP的列表
    return yes_list

'''
只弄了西刺首页的一些IP
存储的IP文本是没有清洗的
自己正则弄一弄
'''

if __name__=='__main__':
    ipList=getIp()
    #得到有效IP列表
    yes_list=testConnect(ipList)
    # 保存到text
    with open('proxy.text','a') as f:
        for i in yes_list:
            IP = i[0].swapcase() + '://' + i[1] + ':' + i[2]
            f.write(IP+'\n')
            print(IP)
    print("ip文本保存完毕")






