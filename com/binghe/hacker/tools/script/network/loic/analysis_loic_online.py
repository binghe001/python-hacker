#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 实时检测DDos攻击
#             要识别攻击，需要设置一个不正常的数据包的阈值，如果某一个用户发送到某个地址的数据包的数量超过
#             这个阈值，就可以把它视为攻击做进一步调查。尽管这并不是绝对证明攻击是用户主动发起的
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket
THRESH = 10000

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