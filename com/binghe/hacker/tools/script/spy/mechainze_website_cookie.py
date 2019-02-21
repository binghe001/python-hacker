#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 打印网站的cookie
# 博客 https://blog.csdn.net/l1028386804

import mechanize
import cookielib

def printCookies(url):
    browser = mechanize.Browser()
    cookie_jar = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookie_jar)
    page = browser.open(url)
    for cookie in cookie_jar:
        print cookie

if __name__ == '__main__':
    url = 'http://www.csdn.net'
    printCookies(url)