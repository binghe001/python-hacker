#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 从网站上下载图片，并直接写入硬盘
# 博客 https://blog.csdn.net/l1028386804

from mechainze_browser import *
from BeautifulSoup import  BeautifulSoup
import optparse
import os

def mirrorImages(url, dir):
    ab = AnonBrowser()
    ab.anonymize()
    html = ab.open(url)
    soup = BeautifulSoup(html)
    image_tags = soup.findAll('img')
    for image in image_tags:
        filename = image['src'].lstrip('http://')
        filename = os.path.join(dir, filename.replace('/', '_'))
        print '[+] Saving ' + str(filename)
        data = ab.open(image['src']).read()
        ab.back()
        save = open(filename, 'wb')
        save.write(data)
        save.close()

def main():
    parser = optparse.OptionParser('usage%prog -u <target url> -d <destination directory>')
    parser.add_option('-u', dest='tgtURL', type='string', hrlp='specify target url')
    parser.add_option('-d', dest='dir', type='string', help='specify destina directory')
    (options, args) = parser.parse_args()
    url = options.tgtURL
    dir = options.dir
    if url == None or dir == None:
        print parser.usage
        exit(0)
    else:
        try:
            mirrorImages(url, dir)
        except Exception, e:
            print '[-] Error Mirroring Images.'
            print '[-] ' + str(e)

if __name__ == '__main__':
    main()
