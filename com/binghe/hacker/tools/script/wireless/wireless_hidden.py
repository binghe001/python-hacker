#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 找出隐藏的802.11网络的网络名
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

#隐藏网络的Mac地址
hiddenNets = []
#已经找到网络名的隐藏网络
unhiddenNets = []
'''
发现一个没有名字的802.11信标帧时，把它添加到hiddenNets中，发现一个802.11 probe响应帧时，就提取它的名字。
我们要查找hiddenNets数据，看在该数组中是否有它的记录，还要查看unhiddenNets数组，看在该数组中是不是没有它
的记录。如果两个条件都能被满足，我们就解析出网络名，并把它显示在屏幕上
'''
def sniffDot11(p):
    if p.haslayer(Dot11ProbeResp):
        addr2 = p.getlayer(Dot11).addr2
        if (addr2 in hiddenNets) & (addr2 not in unhiddenNets):
            netName = p.getlayer(Dot11ProbeResp).info
            print '[+] Decloaked Hidden SSID: ' + netName + ' for MAC: ' + addr2
            unhiddenNets.append(addr2)

    if p.haslayer(Dot11Beacon):
        if p.getlayer(Dot11Beacon).info == '':
            addr2 = p.getlayer(Dot11).addr2
            if addr2 not in hiddenNets:
                print '[-] Detected Hidden SSID: ' + ' with MAC:' + addr2
            hiddenNets.append(addr2)

def main():
    parser = optparse.OptionParser('usage % prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print(parser.usage)
        exit(0)
    else:
        interface = options.interface
    sniff(iface=interface, prn=sniffDot11)

if __name__ == '__main__':
    main()