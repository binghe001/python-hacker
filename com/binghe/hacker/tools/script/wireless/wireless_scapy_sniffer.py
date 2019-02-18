#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 侦听无线网卡数据流量，每侦听到一个数据包，脚本就会运行pktPrint()函数。如果这个数据包是802.11
#             信标，802.11探查(Probe)响应、TCP数据包、DNS流量，那么该函数就输出一个相应的信息。
#             运行脚本前，先使用airmon-ng start wlan0 将wlan0网卡设置为监听模式
#             用法： python wireless_scapy_sniffer.py -i <设置为监听模式的网卡>
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

def pktPrint(pkt):
    if pkt.haslayer(Dot11Beacon):
        print '[+] detected 802.11 Beacon Frame'
    elif pkt.haslayer(Dot11ProbeReq):
        print '[+] Detected 802.11 Probe Request Frame'
    elif pkt.haslayer(TCP):
        print '[+] Detected a TCP Packet'
    elif pkt.haslayer(DNS):
        print '[+] Detected a DNS Packet'

def main():
    parser = optparse.OptionParser("usage%prog -i <iface>")
    parser.add_option("-i", dest='iface', type='string', help='specify iface')
    (options, args) = parser.parse_args()
    iface = options.iface
    if iface == None:
        iface = 'wlan0mon'

    conf.iface = iface
    sniff(prn=pktPrint)

if __name__ == '__main__':
    main()
