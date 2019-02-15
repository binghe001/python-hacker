#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 使用dpkt分析pcap数据包
#             dpkt下载地址为：https://github.com/kbandla/dpkt
#             用法： python analysis_pcap_dpkt.py -p <pcap文件的路径>
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket
import optparse

#打印pcap
def printPcap(pcap):
    for(ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Enthernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print '[+] Src: ' + src + ' ---> Dst: ' +dst
        except:
            pass


#主函数
def main():
    parser = optparse.OptionParser("usage%prog -p <pcap file path>")
    parser.add_option('-p', dest='pcapFilePath', type='string', help='specify pcap file path')
    (options, args) = parser.parse_args()
    pcapFilePath = options.pcapFilePath
    if pcapFilePath == None:
        print parser.usage
        exit(0)

    f = open(pcapFilePath)
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()