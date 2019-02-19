#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 抓取Google搜索数据并实施显示的无线网络数据包嗅探器脚本
#             注意：我们这里用sniff()函数过滤TCP流量中与80端口相关的流量。
#                  Google也在443端口上发送HTTPS流量，但由于HTTPS中的载荷是加密的，
#                  获取它们并没有什么用处
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

def findGoogle(pkt):
    if pkt.haslayer(Raw):
        payload = pkt.getlayer(Raw).load
        if 'GET' in payload:
            if 'google' in payload:
                r = re.findall(r'(?i)\&q=(.*?)\&', payload)
                if r:
                    search = r[0].split('&')[0]
                    search = search.replace('q=', '').replace('+',' ').replace('%20', ' ')
                    print '[+] Searched For: ' + search

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
        print '[*] Starting Google Sniffer.'
        sniff(filter='tcp port 80', prn=findGoogle)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()