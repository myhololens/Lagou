#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import random
import datetime, threading, requests
from bs4 import BeautifulSoup
import os
import settings

# ------------------------------------------------------文档处理--------------------------------------------------------
# 写入文档
def write(path,text):
    with open(path,'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt
# ----------------------------------------------------------------------------------------------------------------------
# 计算时间差,格式: 时分秒
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
# ----------------------------------------------------------------------------------------------------------------------
# 返回一个随机的请求头 headers
def getheaders():
    user_agent_list = settings.MY_USER_AGENT
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers
# -----------------------------------------------------检查ip是否可用----------------------------------------------------
def checkip(targeturl,ip):
    headers =getheaders()  # 定制请求头
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    try:
        response=requests.get(url=targeturl,proxies=proxies,headers=headers,timeout=5).status_code
        if response == 200 :
            return True
        else:
            return False
    except:
        return False

#-------------------------------------------------------获取代理方法----------------------------------------------------
# 免费代理 XiciDaili
def findip(type,pagenum,targeturl,path): # ip类型,页码,目标url,存放ip的路径
    list={'1': 'http://www.xicidaili.com/nt/', # xicidaili国内普通代理
          '2': 'http://www.xicidaili.com/nn/', # xicidaili国内高匿代理
          '3': 'http://www.xicidaili.com/wn/', # xicidaili国内https代理
          '4': 'http://www.xicidaili.com/wt/'} # xicidaili国外http代理
    url=list[str(type)]+str(pagenum) # 配置url
    headers = getheaders() # 定制请求头
    html=requests.get(url=url,headers=headers,timeout = 5).text
    soup=BeautifulSoup(html,'lxml')
    all=soup.find_all('tr',class_='odd')
    for i in all:
        t=i.find_all('td')
        ip=t[1].text+':'+t[2].text
        is_avail = checkip(targeturl,ip)
        if is_avail == True:
            write(path=path,text=ip)
            print(ip)

#-----------------------------------------------------多线程抓取ip入口---------------------------------------------------
def getip(targeturl,path):
     truncatefile(path) # 爬取前清空文档
     start = datetime.datetime.now() # 开始时间
     threads=[]
     for type in range(4):   # 四种类型ip,每种类型取前三页,共12条线程
         for pagenum in range(3):
             t=threading.Thread(target=findip,args=(type+1,pagenum+1,targeturl,path))
             threads.append(t)
     print('开始爬取代理ip')
     for s in threads: # 开启多线程爬取
         s.start()
     for e in threads: # 等待所有线程结束
         e.join()
     print('爬取完成')
     end = datetime.datetime.now() # 结束时间
     diff = gettimediff(start, end)  # 计算耗时
     ips = read(path)  # 读取爬到的ip数量
     print('一共爬取代理ip: %s 个,共耗时: %s \n' % (len(ips), diff))

#-------------------------------------------------------启动-----------------------------------------------------------
if __name__ == '__main__':
    path = 'ip.txt' # 存放爬取ip的文档path
    targeturl = 'http://www.baidu.com' # 验证ip有效性的指定url
    getip(targeturl,path)

# proxy_list = open(os.getcwd()+'/ip.txt').readlines()
# print(random.choice(proxy_list))