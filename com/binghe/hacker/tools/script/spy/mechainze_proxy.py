#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description mechainze代理
# 博客 https://blog.csdn.net/l1028386804

import mechanize

def testProxy(url, proxy):
    browser = mechanize.Browser()
    browser.set_proxies(proxy)
    page = browser.open(url)
    source_code = page.read()
    print source_code

url = 'http://ip.netsc.noaa.gov'
hideMeProxy = {'http': '216,155.139.115:3128'}
testProxy(url, hideMeProxy)