#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 用Scapy找出Domain Flux流量
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *

def dnsQRTest(pkt):
    if pkt.haslayer(DNSRR) and pkt.getlayer(UDP).sport==53:
        rcode = pkt.getlayer(DNS).rcode
        qname = pkt.getlayer(DNSQR).qname
        if rcode == 3:
            print '[!] Name request lookup failed: ' + qname
            return True
        else:
            return False

def main():
    parser = optparse.OptionParser('usage%prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string', help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    pkts = rdpcap(pcapFile)
    for pkt in pkts:
        if dnsQRTest(pkt):
            unAnsReqs = unAnsReqs + 1
            print '[!] ' + str(unAnsReqs) + ' Total Unanswered Name Requests'

if __name__ == '__main__':
    main()