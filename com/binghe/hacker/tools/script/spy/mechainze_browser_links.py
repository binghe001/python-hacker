#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 分析并打印网页上的链接
# 博客 https://blog.csdn.net/l1028386804

from mechainze_browser import *
from BeautifulSoup import BeautifulSoup
import optparse
import re

#获取html页面
def get_html(url):
    ab = AnonBrowser()
    page = ab.open(url)
    html = page.read()
    return html

#利用正则表达式搜索网页链接并打印
def printLinksByRe(html):
   try:
       print '[+] Printing Links From Regex.'
       link_finder = re.compile('href="(.*?)"')
       links = link_finder.findall(html)
       for link in links:
           print link
   except:
       pass

#利用BeautifulSoup
def printLinksByBeautifulSoup(html):
    try:
        print '\n[+] Printing Links From BeautifulDoup.'
        soup = BeautifulSoup(html)
        links = soup.findAll(name='a')
        for link in links:
            if link.has_key('href'):
                print link['href']
    except:
        pass

def printLinks(url):
    html = get_html(url)
    printLinksByRe(html)
    printLinksByBeautifulSoup(html)

def main():
    parser = optparse.OptionParser('usage%prog -u <target url>')
    parser.add_option('-u', dest='tgtURL', type='string', help='specify target url')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    if url == None:
        print parser.usage
        exit(0)
    else:
        printLinks(url)

if __name__ == '__main__':
    main()


