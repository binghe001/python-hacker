#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 读取TCP序列号
#             依次出现的SYN-ACK包中的TCP序列号之间的差值均为128000
#             用法： python scapy_syn_tcp.py -t <目标ip>
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

#接收目标IP地址，返回下一个SYN-ACK包的序列号(当前SYN-ACK包的序列号加上差值)
def calTSN(tgt):
    seqNum = 0
    preNum = 0
    diffSeq = 0
    for x in range(1, 5):
        if preNum != 0:
            preNum = seqNum
        pkt = IP(dst=tgt) / TCP()
        ans = sr1(pkt, verbose=0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        print '[+] TCP Seq Difference: ' + str(diffSeq)
    return seqNum + diffSeq

def main():
    parser = optparse.OptionParser('usage%prog -t <target ip>')
    parser.add_option('-t', dest='tarIP', type='string', help='specify target ip')
    (options, args) = parser.parse_args()
    tarIP = options.tarIP
    if tarIP == None:
        print parser.usage
        exit(0)
    seqNum = calTSN(tarIP)
    print '[+] Next TCP Sequence Number to ACK is: ' + str(seqNum + 1)

if __name__ == '__main__':
    main()