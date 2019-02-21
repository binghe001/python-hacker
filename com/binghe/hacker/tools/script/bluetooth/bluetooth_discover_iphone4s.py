#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/20
# Created by 冰河
# Description 识别处于“不可被发现”模式下的苹果iPhone手机的蓝牙
#             侦听MAC的前三个十六进制数属于iPhone 4S的802.11数据帧，如果检测到，就把结果打印到屏幕，并把802.11帧中的Mac地址保存下来
#             寻找“不可被发现”模式的iPhone蓝牙信号小技巧：在iPhone里，把无线网卡的Mac地址加1，就得到了这台iPhone的蓝牙Mac
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
from bluetooth import *

#根据iPhone无线Mac地址计算蓝牙Mac地址
def retBtAddr(addr):
    btAddr = str(hex(int(addr.replace(':', ''),16) + 1))[2:]
    btAddr = btAddr[0:2] + ':' + btAddr[2:4] + ':' + btAddr[4:6] + ':' + btAddr[6:8] + ':' + btAddr[8:10] + ':' + btAddr[10:12]
    return btAddr

#检测蓝牙设备
def checkBluetooth(btAddr):
    btName = lookup_name(btAddr)
    if btName:
        print '[+] Detected Bluetooth Device: ' + btName
    else:
        print '[-] Failed to Detect Bluetooth Device.'

def wifiPrint(pkt):
    #苹果公司使用的三个十六进制数
    iPhone_OUI = 'd0:23:db'
    if pkt.haslayer(Dot11):
        wifiMac = pkt.getlayer(Dot11).addr2
        if iPhone_OUI == wifiMac[:8]:
            print '[*] Detected iPhone Mac: ' + wifiMac
            btAddr = retBtAddr(wifiMac)
            print '[+] Testing Bluetooth MAC: ' + btAddr
            checkBluetooth(btAddr)

conf.iface = 'wlan0mon'
sniff(prn=wifiPrint)
