#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/20
# Created by 冰河
# Description 发现周围的蓝牙设备，并把蓝牙设备的名字和Mac地址输出到屏幕
# 博客 https://blog.csdn.net/l1028386804

from bluetooth import *

devList = discover_devices()
for device in devList:
    name = str(lookup_name(device))
    print "[+] Found Blutooth Device " + str(name)
    print "[+] Mac Address:" + str(device)