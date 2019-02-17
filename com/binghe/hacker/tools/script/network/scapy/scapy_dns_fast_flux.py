#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 用Scapy找出flux流量
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

dnsRecords = {}

def handlePkt(pkt):
    if pkt.haslayer(DNSRR):
        rrname = pkt.getlayer(DNSRR).rrname
        rdata = pkt.getlayer(DNSRR).rdata
        if dnsRecords.has_key(rrname):
            if rdata not in dnsRecords[rrname]:
                dnsRecords[rrname].append(rdata)
        else:
            dnsRecords[rrname] = []
            dnsRecords[rrname].append(rdata)

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
        handlePkt(pkt)
    for item in dnsRecords:
        print '[+] ' + item + ' has ' + str(len(dnsRecords[item])) + ' unique IPs.'

if __name__ == '__main__':
    main()