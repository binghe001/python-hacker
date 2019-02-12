#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/12
# Created by 冰河
# Description 连接ssh
# 博客 https://blog.csdn.net/l1028386804

import pexpect

PROMPT=['# ', '>>> ', '> ', '\$ ']

#向目标主机SSH会话发送执行的命令
def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print child.before

#连接目标主机
def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    #超时，返回0
    if ret == 0:
        print '[-] Error Connecting'
        return

    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])

    if ret == 0:
        print '[-] Error Connecting'
        return

    child.sendline(password)
    child.expect(PROMPT)
    return child

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