#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/14
# Created by 冰河
# Description 列举Windows注册表中存储的网络名和默认网关的Mac,并通过https://wigle.net查询物理位置
#             用法：python windows_reg_net_location.py -u username -p password
# 博客 https://blog.csdn.net/l1028386804

import optparse
import mechanize
import urllib
import re
import urlparse
from _winreg import *

search_lat = r'maplat=.*\&'
search_lon = r'maplon=.*\&'

#将Windows注册表中的REG_BINARY值转换成一个实际的MAC地址
def val2addr(val):
    addr = ''
    for ch in val:
        addr += ("%02x " % ord(ch))
    addr = addr.strip(" ").replace(" ",":")[0:17]
    return addr

#创建一个mechanize浏览器实例，接下来，打开wigle.net主页。然后在Wigle登录页面请求登录
#把用户名和密码放在请求的参数里发送过去。在成功登录之后，我们创建一个HTTP Post请求，把
#要查询的Mac地址放在netid参数中。在收到HTTP post请求的响应结果之后，我们搜索字符串
#"maplat="和"maplon="以获取精度和纬度坐标，在得到它们之后就把它们打印出来
#username:登录wigle.net的用户名
#password:登录wigle.net的密码
#netid:要查询的Mac地址
def wiglePrint(username, password, netid):
    browser = mechanize.Browser()
    browser.open('https://wigle.net')
    #构造请求数据
    reqData = urllib.urlencode({'credential_0':username, 'credential_1':password})
    #请求登录
    browser.open('https://wigle.net/gps/gps/main/login', reqData)
    params = {}
    params['netid'] = netid
    reqParams = urllib.urlencode(params)
    respURL = 'https://wigle.net/gps/gps/main/confirmquery/'
    resp = browser.open(respURL, reqParams).read()
    print str(resp)
    mapLat = 'N/A'
    mapLon = 'N/A'
    rLat = re.findall(search_lat, resp)
    if rLat:
        mapLat = rLat[0].split('&')[0].split('=')[1]
    rLon = re.findall(search_lon, resp)
    if rLon:
        mapLon = rLon[0].split
    print '[-] Lat: ' + mapLat + ', Lon: ' + mapLon

#打印网络信息
def printNets(username, password):
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
            #获取地理位置
            wiglePrint(username, password, macAddr)
            CloseKey(netKey)
        except:
            break

def main():
    parser = optparse.OptionParser("usage%prog -u <wigle username> -p <wigle password>")
    parser.add_option('-u', dest='username', type='string', help='specify wigle username')
    parser.add_option('-p', dest='password', type='string', help='specify wigle password')
    (options, args) = parser.parse_args()
    username = options.username
    password = options.password
    if username == None or password == None:
        print parser.usage
        exit(0)
    else:
        printNets(username, password)



if __name__ == '__main__':
    main()