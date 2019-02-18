#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 产生大量警报的工具包，分析人员也可以使用这个工具来验证IDS是否能够正确识别出恶意流量
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

def ddosTest(src, dst, iface, count):
    pkt = IP(src=src,dst=dst)/ICMP(type=8,id=678)/Raw(load='1234')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / ICMP(type=0) / Raw(load='AAAAAAAAAA')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / UDP(dport=31335) / Raw(load='PONG')
    send(pkt, iface=iface, count=count)
    pkt = IP(src=src, dst=dst) / ICMP(type=0, id=456)
    send(pkt, iface=iface, count=count)

def main():
    parser = optparse.OptionParser('usage%prog -s <source ip> -t <target ip> -i <iface> -c <count>')
    parser.add_option('-s', dest='srcIP', type='string', help='specify source ip')
    parser.add_option('-t', dest='tarIP', type='string', help='specify target ip')
    parser.add_option('-i', dest='iface', type='string', help='specify iface')
    parser.add_option('-c', dest='count', type='int', help='specify count')
    (options, args) = parser.parse_args()
    srcIP = options.srcIP
    tarIP = options.tarIP
    if srcIP == None or tarIP == None:
        print parser.usage
        exit(0)

    iface = options.iface
    if iface == None:
        iface = 'eth0'
    count = options.count
    if count <= 0:
        count = 1

    ddosTest(srcIP, tarIP, iface, count)

if __name__ == '__main__':
    main()


