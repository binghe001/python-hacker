#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 检测数据包中的TTL值是否为假，如果是假的则打印出来，此脚本可检测nmap是否启用了伪装源IP扫描
# 博客 https://blog.csdn.net/l1028386804

import time
import optparse
from scapy.all import *
from IPy import IP as IPTEST

ttlvalues={}
THRESH = 5

'''
接收两个参数：源IP地址及TTL值，如果TTL值不正确，则输出一条消息。首先，用一个快速的条件语句把使用内网/私有
IP(10.0.0.0~10.255.255.255、172.16.0.0~172.31.255.255、192.168.0.0~192.168.255.255)的数据包
全部去掉。要做到这一点，需要导入IPy库，为了避免IPy库中的IP类与Scapy库中的IP类冲突，我们把它重命名为IPTEST
类。如果IPTEST(ipsrc).iptype()返回"PRIVATE",我们就让checkTTL函数返回，并忽略对数据包的检查。

我们可能受到来自同一个源地址的多个数据包，而我们又不想重复检查同一个源地址。如果我们之前从未见过这个源地址，
则要构建一个目标IP地址为这个源地址的IP包，这个包应该是一个ICMP请求包，这样目标主机就会做出回应。一旦目标主机
做出了响应，我们就把TTL值存储在一个用源ip地址作为索引的词典中。然后将实际收到的TTL与原始数据包中的TTL放在一起，
判断它们的差值是否超过了一个阈值。走不通的路径到达目标主机的数据包所经过的路由设备的数量可能会有所差异，因此其
TTL也可能不完全一样。但是，如果中继跳数的差超过了5跳，则可以推断该TTL是假的，并在屏幕上输出一条警告消息。
'''
def checkTTL(ipsrc, ttl):
    if IPTEST(ipsrc).iptype() == 'PRIVATE':
        return
    if not ttlvalues.has_key(ipsrc):
        pkt = sr1(IP(dst=ipsrc) / ICMP(), retry=0, timeout=1, verbose=0)
        ttlvalues[ipsrc] = pkt.ttl

    if abs(int(ttl) - int(ttlvalues[ipsrc])) > THRESH:
        print '\n[!] Detected Possible Spoofed Packet From: ' + ipsrc
        print '[!] TTL: ' + ttl + ', Actual TTL: ' + str(ttlvalues[ipsrc])

#解析收到的数据包的源ip和ttl
def testTTL(pkt):
    try:
        if pkt.haslayer(IP):
            ipsrc = pkt.getlayer(IP).src
            ttl = str(pkt.ttl)
            checkTTL(ipsrc,ttl)
    except:
        pass

def main():
    parser = optparse.OptionParser("usage%prog -i <interface> -t <thresh>")
    parser.add_option('-i', dest='iface', type='string', help='specify network interface')
    parser.add_option('-t', dest='thresh', type='int', help='specify threshod count')
    (options, args) = parser.add_option()
    if options.iface == None:
        conf.iface = 'eth0'
    else:
        conf.iface = options.iface

    if options.thresh == None:
        THRESH = 5
    else:
        THRESH = options.thresh

    sniff(prn=testTTL, store=0)

if __name__ == '__main__':
    main()


