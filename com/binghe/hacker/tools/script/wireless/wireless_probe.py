#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 发现802.11请求
#             用法： python wireless_probe.py -i <处于监听模式的无线网卡>
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

probeReqs = []

#嗅探802.11Probe数据包
def sniffProbe(p):
    if p.haslayer(Dot11ProbeReq):
        netName = p.getlayer(Dot11ProbeReq).info
        if netName not in probeReqs:
            probeReqs.append(netName)
            print '[+] Detected New Probe Request: ' + netName

def main():
    parser = optparse.OptionParser('usage%prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface listen to')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print parser.usage
        exit(0)
    else:
        interface = options.interface

    #嗅探数据包
    sniff(iface=interface, prn=sniffProbe)

if __name__ == '__main__':
    main()