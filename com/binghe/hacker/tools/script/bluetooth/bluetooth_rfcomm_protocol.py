#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 使用蓝牙服务发现协议打印蓝牙设备的服务名称、协议和端口号
# 博客 https://blog.csdn.net/l1028386804

from bluetooth import *

def sdpBrowse(addr):
    services = find_service(address=addr)
    for service in services:
        name = service['name']
        proto = service['protocol']
        port = str(service['port'])
        print '[+] Found ' + str(name) + ' on ' + str(proto) + ':' + port

sdpBrowse('00:16:38:DE:AD:11')