#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 检测RFCOMM通道是否开放并处于监听状态
# 博客 https://blog.csdn.net/l1028386804

from bluetooth import *

#这里，我们向connect()函数传递一个含有MAC地址和目标端口的元组(tuple)。如果连接成功，就知道该RFCOMM通道是开放的
#且处于监听状态，如果函数抛出一个异常，证明无法连接到该端口

def rfcommCon(addr, port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr, port))
        print '[+] RFCOMM Port ' + str(port) + ' open'
        sock.close()
    except Exception, e:
        print '[-] RFCOMM Port ' + str(port) + ' closed'

for port in range(1, 30):
    rfcommCon('00:16:38:DE:AD:11', port)