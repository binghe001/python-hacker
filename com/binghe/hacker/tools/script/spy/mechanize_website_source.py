#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 用mechanize解析网站源代码
# 博客 https://blog.csdn.net/l1028386804

import mechanize

def viewPage(url):
    browser = mechanize.Browser()
    page = browser.open(url)
    source_code = page.read()
    print source_code

if __name__ == '__main__':
    viewPage('https://www.csdn.net')