#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/14
# Created by 冰河
# Description 列举Windows注册表中存储的网络名和默认网关的Mac,
#             即：把存储在Windows注册表中的之前连过的那些无线网络列举出来
# 博客 https://blog.csdn.net/l1028386804


from _winreg import *

#将Windows注册表中的REG_BINARY值转换成一个实际的MAC地址
def val2addr(val):
    addr = ''
    for ch in val:
        addr += ("%02x " % ord(ch))
    addr = addr.strip(" ").replace(" ",":")[0:17]
    return addr

#打印网络信息
def printNets():
    net = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print '\n[*] Networks you have Joined.'
    for i in range(100):
        try:
            guid = EnumKey(key, i)
            netKey = OpenKey(key, str(guid))
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            macAddr = val2addr(addr)
            netName = str(name)
            print '[+] ' + netName + ' ' + macAddr
            CloseKey(netKey)
        except:
            break

def main():
    printNets()

if __name__ == '__main__':
    main()