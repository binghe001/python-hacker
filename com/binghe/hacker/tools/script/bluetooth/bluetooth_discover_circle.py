#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/20
# Created by 冰河
# Description 持续监听新的蓝牙设备
#             这里用一个名为alreadyFound的数组来记录已经被找到的设备
# 博客 https://blog.csdn.net/l1028386804

import time
from bluetooth import *
alreadyFound = []

def findDevs():
    foundDevs = discover_devices(lookup_names=True)
    for (addr, name) in foundDevs:
        if addr not in alreadyFound:
            print '[*] Found Bluetooth Device: ' + str(name)
            print '[+] Mac address: ' + str(addr)
            alreadyFound.append(addr)

while True:
    findDevs()
    time.sleep(5)
