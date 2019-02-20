#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/20
# Created by 冰河
# Description 检测企图盗用Wordpress会话的人，并将结果显示在屏幕上
# 博客 https://blog.csdn.net/l1028386804

import re
import optparse
from scapy.all import *

cookieTable = {}

def fireCatcher(pkt):
    raw = pkt.sprintf('%Raw.load%')
    r = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if r and 'Set' not in raw:
        if r[0] not in cookieTable.keys():
            cookieTable[r[0]] = pkt.getlayer(IP).src
            print '[+] Detected and indexed cookie.'
        elif cookieTable[r[0]] != pkt.getlayer(IP).src:
            print '[*] Detected Conflict for ' + r[0]
            print 'Victim = ' + cookieTable[r[0]]
            print 'Attacker = ' + pkt.getlayer(IP).src


def main():
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print parser.usage
        exit(0)
    else:
        conf.iface = options.interface

    try:
        sniff(filter='tcp port 80', prn=fireCatcher)
    except KeyboardInterrupt:
        exit(0)

    if __name__ == '__main__':
        main()

