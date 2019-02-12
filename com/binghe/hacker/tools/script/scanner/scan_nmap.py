#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/12
# Created by 冰河
# Description 使用nmap进行扫描
#             用法: python scan_nmap01.py -H 10.2.2.250 -p 21,22,80,443,135,445
#                  python scan_nmap01.py -H 10.2.2.250 -p 21
#             注意: 扫描多端口，端口与端口之间不要有空格
# 博客 https://blog.csdn.net/l1028386804

import nmap
import optparse

#利用nmap进行扫描
def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print " [*] " + tgtHost + " tcp/" + tgtPort + " " + state

#主函数，解析参数并调用扫描方法
def main():
    parser = optparse.OptionParser("usage%prog " + "-H <target host> -p <target port>")
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s]')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(",")

    if (tgtHost == None) | (tgtPorts[0] == None):
        print  parser.usage
        exit(0)

    for tgtPort in tgtPorts:
        nmapScan(tgtHost, tgtPort)

#程序入口
if __name__ == '__main__':
    main()


