#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 使用GeoLiteCity.dat数据库查询指定IP的位置信息
# 博客 https://blog.csdn.net/l1028386804

import pygeoip

out_exit = 'exit'
out_quit = 'quit'

#获取geoip数据库实例对象
def get_geoip():
    return pygeoip.GeoIP("GeoLiteCity.dat")

#打印IP信息
def printRecord(tgt, gi):
    rec = gi.record_by_name(tgt)
    print rec
    city = rec['city']
    region = rec['time_zone']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print '[*] Target: ' + tgt + ' Geo-located. '
    print '[+] ' + str(city) + ', ' + str(region) + ', ' + str(country)
    print '[+] Latitude: ' + str(lat) + ', Longitude: ' + str(long)

#搜索IP信息
def search_ip_info(gi):
    while True:
        tgt = raw_input("\nPlease Input IP, If You Want to Exit, Please Input exit or quit: ")
        while not tgt:
            tgt = raw_input("\nPlease Input IP, If You Want to Exit, Please Input exit or quit: ")

        # 退出程序
        if tgt == out_exit or tgt == out_quit:
            exit(0)
        printRecord(tgt, gi)

#主函数
def main():
    #实例化GeoIP对象
    gi = get_geoip()
    search_ip_info(gi)

if __name__ == '__main__':
    main()




