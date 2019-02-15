#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/15
# Created by 冰河
# Description 查询火狐浏览器存储的上网记录
#             在Windows系统中，火狐把历史记录存放在C:\Documents and Settings\<USER>\Application Data\Mozilla\Firefox\Profiles\<profile folder>\目录中
#             在Mac OS X系统中，火狐把历史记录存放在：/Users/<USER>/Library/Application/Support/Forefox/Profiles/<profile folder>目录中
#             用法： python meta_firefox_sqlite3.py -p <路径>
# 博客 https://blog.csdn.net/l1028386804

import re
import optparse
import os
import sqlite3

#打印下载记录
def printDownloads(downloadDB):
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    c.execute('SELECT name, source, datetime(endTime / 1000000, \'unixepoch\') FROM moz_downloads;')
    print '\n[*] --- Files Downloaded --- '
    for row in c:
        print '[+] File: ' + str(row[0]) + ' from source: ' + str(row[1]) + ' at: ' + str(row[2])

#打印Cookies
def printCookies(cookieDB):
    try:
        conn = sqlite3.connect(cookieDB)
        c= conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies;')
        print '\n[*] -- Found Cookies --'

        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print '[+] Host: ' + host + ', Cookie: ' + name + ', Value: ' + value

    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'

#打印历史记录
def printHistory(placeDB):
    try:
        conn = sqlite3.connect(placeDB)
        c = conn.cursor()
        c.execute("SELECT url, datetime(visit_date / 1000000, 'unixepoch') FROM moz_places, moz_historyvisits where visit_count > 0 AND  moz_places.id = moz_hostoryvisits.place_id; ")
        print '\n[*] -- Found History --'
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print '[+] ' + date + '- Visited: ' + url
    except Exception, e:
        if 'encrypted' in str(e):
            print '\n[*] Error reading your cookies database.'
            print '[*] Upgrade your Python-Sqlite3 Library'
            exit(0)

#打印google搜索记录
def printGoogle(placesDB):
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    c.execute("SELECT url, datetime(visit_date / 1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE moz_places.visit_count > 0 AND moz_places.id = moz_historyvisits.place_id;")
    print  '\n[*] -- Found Google --'
    for row in c:
        url = str(row[0])
        date = str(row[1])
        if 'google' in url.lower():
            r = re.findall(r'q=.*\&', url)
            if r:
                search = r[0].split('&')[0]
                search = search.replace('q=','').replace('+',' ')
                print '[+] ' + date + ' - Searched For: ' + search

#主函数
def main():
    parser = optparse.OptionParser("usage%prog -p <firefox profile path>")
    parser.add_option('-p', dest='pathName', type='string', help='specify firefox profile path')
    (options, args) = parser.parse_args()
    pathName = options.pathName
    if pathName == None:
        print parser.usage
        exit(0)
    elif os.path.isdir(pathName) == False:
        print '[!] Path does Not Exist: ' + pathName
        exit(0)
    else:
        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        if os.path.isfile(downloadDB):
            printDownloads(downloadDB)
        else:
            print '[!] Downloads DB does not exist: ' + downloadDB

        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        if os.path.isfile(cookiesDB):
            printCookies(cookiesDB)
        else:
            print '[!] Cookies DB does not exist: ' +cookiesDB

        placesDB = os.path.join(pathName, 'places.sqlite')
        if os.path.isfile(placesDB):
            printHistory(placesDB)
            printGoogle(placesDB)
        else:
            print  '[!] PlacesDB does not exist: ' + placesDB

if __name__ == '__main__':
    main()


