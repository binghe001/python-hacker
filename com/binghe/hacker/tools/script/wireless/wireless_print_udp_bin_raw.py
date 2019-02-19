#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 打印目标端口为5556的UDP数据包二进制数据
#             python wireless_print_udp_bin_raw.py -i <处于监听模式的网卡>
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

NAVPORT = 5556

def printPkt(pkt):
    if pkt.haslayer(UDP) and pkt.getlayer(UDP).dport == NAVPORT:
        raw = pkt.sprintf('%Raw.load%')
        print raw

def main():
    parser = optparse.OptionParser('usage % prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.iface = options.interface

    sniff(prn=printPkt)