#!/usr/bin/env python
# -*- coding: gbk -*-
# -*- coding: utf-8 -*-
# Date: 2019/2/12
# Created by 冰河
# Description 端口扫描器  用法：  python xxx.py -H targetHost -p targetPort[s]
#                              python scan_hosts01.py -H 10.2.2.250 -p 21,22,80,443,135,445
#                              python scan_hosts01.py -H 10.2.2.250 -p 21
#                       注意: 扫描多端口，端口与端口之间不要有空格
# 博客 https://blog.csdn.net/l1028386804

import optparse
from socket import *
from threading import *

#信号量
screenLock = Semaphore(value=1)

#连接目标主机和端口，连接成功打印目标端口开放，连接不成功则打印目标端口关闭
def connScan(tgtHost, tgtPort):
    try:
        # print '\n[*] Scanning port ' + str(tgtPort)
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        #向项目主机的特定端口发送一个数据串并等待响应，跟进收集到的响应，可以推断出在目标主机和端口上运行的应用
        connSkt.send('ViolentPython\r\n')
        #接收响应信息
        results = connSkt.recv(100)
        #对信号量加锁，保证在同一个时间只有一个线程打印输出
        screenLock.acquire()
        print '\n[+] %d/tcp open' % tgtPort
        print '[+] ' + str(results)

    except:
        #信号量加锁，保证在同一个时间只有一个线程打印输出
        screenLock.acquire()
        print '\n[-] %d/tcp closed' % tgtPort
    finally:
        #释放锁
        screenLock.release()
        connSkt.close()

#扫描目标主机指定的端口列表
def portScan(tgtHost, tgtPorts):
    try:
        #确定主机名对应的IP地址
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s' : Unknown host" % tgtHost
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print '\n[+] Scan Results for: ' + tgtName[0]
    except:
        print '\n[+] Scan Results for: ' + tgtIP

    #设置默认超时时间
    setdefaulttimeout(2)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


#主函数，解析参数并调用端口扫描方法
def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port[s]>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s]')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print '[-] You must specify a target host and port[s]: ' + parser.usage
        exit(0)
    portScan(tgtHost, tgtPorts)

#程序入口
if __name__ == '__main__':
    main()