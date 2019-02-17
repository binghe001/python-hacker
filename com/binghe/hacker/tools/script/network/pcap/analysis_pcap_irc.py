#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/17
# Created by 冰河
# Description 解析HIVE服务器上的IRC命令
#             要发起攻击，“匿名者”成员需要登录到指定的IRC服务器上发出一条攻击指令，
#             如 !lazor targetip=<ip> message=test_test port=80 method=tcp wait=false random=true start
#             导出6667端口的数据流量： tcpdump -i eth0 -A 'port 6667'
#             在获得TCP层部分的数据后，我们检查它的源端口和目标端口是不是6667，如果我们看到!lazor指令的目标端口时6667
#             则可以去确定某个成员提交了一个攻击指令；如果我们看到!lazor指令的源端口为6667，则可以认出这是服务器在向HIVE
#             中的成员发布发动攻击的消息
# 博客 https://blog.csdn.net/l1028386804

import dpkt
import socket

#查询Hive mind
def findHivemind(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            if dport == 6667:
                if '!lazor' in tcp.data.lower():
                    print '[!] DDos Hivemind issued by: ' + src
                    print '[+] Target CMD: ' + tcp.data
            if sport == 6667:
                if '!lazor' in tcp.data.lower():
                    print '[!] DDos Hivemind issued to: ' + src
                    print '[+] Target CMD: ' + tcp.data
        except:
            pass