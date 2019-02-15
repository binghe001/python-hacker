#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 分析pcap文件，并将分析结果生成KML文件在Google地球上标注
#             运行脚本，输出会重定向到一个扩展名为.kml的文本文件，用google地球打开这个文件可以看到，数据包源和目标地址都已推行华的形式展现了出来
#             用法： python analysis_pcap_kml.py -p <pcap文件路径>
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket
import pygeoip
import optparse

#实例化geoip实例，注意要将GeoLiteCity.dat数据库与此脚本放到同一目录下
gi = pygeoip.GeoIP('GeoLiteCity.dat')

#构建并返回kml文件结构
def retKML(ip):
    rec = gi.record_by_name(ip)
    try:
        longitude = rec['longitude']
        latitude = rec['latitude']
        kml = ('<Placemark>\n'
                '<name>%s</name>\n'
                '<Point>\n' 
                '<coordinates>%6f,%6f</coordinates>\n' 
                '</Point>\n'
                '</Placemark>\n'
               ) % (ip, longitude, latitude)
        return kml
    except:
        return ''

#解析IP
def plotIPs(pcap):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            srcKML = retKML(src)
            dst = socket.inet_ntoa(ip.dst)
            dstKML = retKML(dst)
            kmlPts = kmlPts + srcKML + dstKML
        except:
            pass
    return kmlPts

#主函数
def main():
    parser = optparse.OptionParser('usage%prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string', help='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print(parser.usage)
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\
     \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc = kmlheader + plotIPs(pcap) + kmlfooter
    print(kmldoc)

if __name__ == '__main__':
    main()