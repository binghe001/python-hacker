#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/12
# Created by 冰河
# Description 使用pexpect中的pxssh模块连接ssh， 需要在Linux下执行
# 博客 https://blog.csdn.net/l1028386804

from pexpect import pxssh

#向目标主机SSH会话发送执行的命令
def send_command(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before

#连接目标主机
def connect(user, host, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        return s
    except Exception, e:
        print '[-] Error Connecting ==> ' + e
        exit(0)

def main():
    #接收命令行参数
    host = raw_input("Please Input the SSH Host: ")
    while not host:
        host = raw_input("Please Input the SSH Host: ")

    user = raw_input("Please Input Username: ")
    while not user:
        user = raw_input("Please Input Username: ")

    password = raw_input("Please Input Password: ")
    while not password:
        password = raw_input("Please Input Password: ")

    cmd = raw_input("Please Input cmd: ")
    while not cmd:
        cmd = raw_input("Please Input cmd: ")

    child = connect(user, host, password)
    send_command(child, cmd)

if __name__ == '__main__':
    main()