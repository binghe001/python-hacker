#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 分析pcap数据包，可以直接看到数据包的源和目标的物理位置，此脚本是其他三个脚本的最终整合版
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket
import pygeoip
import optparse

#实例化geoip实例，注意要将GeoLiteCity.dat数据库与此脚本放到同一目录下
gi = pygeoip.GeoIP('GeoLiteCity.dat')

#返回指定IP对应的物理位置
def retGeoStr(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        country = rec['country_code3']
        if city != '':
            geoLoc = city + ', ' + country
        else:
            geoLoc = country
        return geoLoc

    except Exception, e:
        return 'Unregistered'

#打印pcap信息
def printPcap(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            print '[+] Src: ' + src + ' --> Dst: ' + dst
            print '[+] Src: ' + retGeoStr(src) + ' --> Dst: ' + retGeoStr(dst)
        except:
            pass

#主函数
def main():
    parser = optparse.OptionParser('usage%prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string', help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    printPcap(pcap)

if __name__ == '__main__':
    main()

