#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 分析loic
#              分析用户是否主动下载LOIC，随后收到一条HIVE指令，接着又发起攻击等一系列行为放在一起，就能
#              充分证明用户参与了“匿名者”发起的DDos攻击。此脚本为analysis_dpkt_loic.py、analysis_loic_online.py
#              analysis_pcap_irc.py 三个脚本的整合
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import optparse
import socket
THRESH = 1000
http_method = 'GET'
file_ext = '.zip'
loic = 'loic'
port = 6667
lazor = '!lazor'

#查看下载情况
def findDownload(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == http_method:
                uri = http.uri.lower()
            if file_ext in uri and loic in uri:
                print '[!] ' + src + ' Downloaded LOIC.'
        except:
            pass

def findHivemind(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            if dport == port:
                if lazor in tcp.data.lower():
                    print '[!] DDos Hivemind issued by: ' + src
                    print '[+] Target CMD: ' + tcp.data
            if sport == port:
                if lazor in tcp.data.lower():
                    print '[!] DDos Hivemind issued to: ' + src
                    print '[+] Target CMD: ' + tcp.data
        except:
            pass

#检测是否攻击
def findAttack(pcap):
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            if dport == 80:
                stream = src + ':' + dst
                if pktCount.has_key(stream):
                    pktCount[stream] = pktCount[stream] + 1
                else:
                    pktCount[stream] = 1
        except:
            pass

    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            print '[+] ' + src + ' attacked ' + dst + ' with ' + str(pktsSent) + ' pkts.'

def main():
    parser = optparse.OptionParser("usage%prog -p <pcap file> -t <thresh>")
    parser.add_option('-p', dest='pcapFile', type='string', help='specify pcap filename')
    parser.add_option('-t', dest='thresh', type='int', help='specify threshold count')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)

    if options.thresh == None:
        THRESH = options.thresh

    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    findDownload(pcap)
    findHivemind(pcap)
    findAttack(pcap)

if __name__ == '__main__':
    main()


