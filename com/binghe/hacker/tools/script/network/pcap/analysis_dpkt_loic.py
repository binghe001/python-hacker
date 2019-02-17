#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 使用Dpkt发现下载LOIC的行为
#             流程为：
#                  解析HTTP流量，并检查其中有无通过HTTP GET获取压缩过的LOIC二进制可执行文件的情况，
#                  如果HTTP层中使用了GET方法，则解析HTTP GET所要获取的统一资源标识符(URI)。如果
#                  该URI所指向的文件的文件名中含有.zip和LOIC，则在屏幕上输出一条某个IP正在下载LOIC的消息
#             Loic下载地址:http://sourceforge.net/projects/loic
#             tcpdump -i eth0 -A 'port 80' 过滤80端口的数据包
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket
import optparse

#发现下载Loic的行为
def findDownLoic(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    print '[!] ' + src + 'Downloaded LOIC.'
        except:
            pass

#主函数
def main():
    parser = optparse.OptionParser("usage%prog -p <pcap file>")
    parser.add_option('-p', dest='pcapFile', type='string', help='specify pcap file.')
    (options, args) = parser.parse_args()
    pcapFile = options.pcapFile
    if pcapFile == None:
        print parser.usage
        exit(0)
    f = open(pcapFile, 'r')
    pcap = dpkt.pcap.Reader(f)
    findDownLoic(pcap)

#入口
if __name__ == '__main__':
    main()



