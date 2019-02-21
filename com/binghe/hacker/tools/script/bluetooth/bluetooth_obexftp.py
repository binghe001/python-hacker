#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 用Python ObexFTP控制打印机
# 博客 https://blog.csdn.net/l1028386804

import obexftp

def controlPrinter(mac, port, img):
    try:
        btPrinter = obexftp.client(obexftp.BLUETOOTH)
        btPrinter.connect(mac,port)
        btPrinter.put_file(img)
        print '[+] Printed Image.'
    except:
        print '[-] Failed to print Image.'

if __name__ == '__main__':
    controlPrinter('00:16:38:DE:AD:11', 2, '/tmp.test.jpg')