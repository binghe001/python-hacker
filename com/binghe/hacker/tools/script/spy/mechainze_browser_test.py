#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 测试自定义浏览器，可打印多个不同的cookie
# 博客 https://blog.csdn.net/l1028386804

from mechainze_browser import *

ab = AnonBrowser(proxies=[], user_agents=[('User-agent', 'superSecretBrowser')])
for attempt in range(1, 5):
    ab.anonymize()
    print '[*] Fetching page'
    response = ab.open('http://www.csdn.net')
    for cookie in ab.cookie_jar:
        print cookie

