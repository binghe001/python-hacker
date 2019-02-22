#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/21
# Created by 冰河
# Description 用正则表达式解析Twitter用户的兴趣爱好
#             用法： python mechainze_twitter_hobby.py -u <twitter handle>
# 博客 https://blog.csdn.net/l1028386804

from mechainze_browser import *
import json
import re
import urllib
import urllib2
import optparse

class ReconPerson:

    def __init__(self, handle):
        self.handle = handle

    def get_tweets(self):
        query = urllib.quote_plus('from:' + self.handle + ' since:2019-02-21 include:retweets')
        tweets = []
        browser = AnonBrowser()
        browser.anonymize()
        response =browser.open('http://search.twitter.com/search.json?q=' + query)
        json_objects = json.load(response)
        for result in json_objects['results']:
            new_result = {}
            new_result['from_user'] = result['from_user_name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            tweets.append(new_result)
        return tweets

    def find_interests(self, tweets):
        interests = {}
        interests['links'] = []
        interests['users'] = []
        interests['hashtags'] = []
        for tweet in tweets:
            text = tweet['tweet']
            links = re.compile('(http.*?)\Z|(http.*?) ').findall(text)
            for link in links:
                if link[0]:
                    link = link[0]
                elif link[1]:
                    link = link[1]
                else:
                    continue
                try:
                    response = urllib2.urlopen(link)
                    full_link = response.url
                    interests['links'].append(full_link)
                except:
                    pass
            interests['users'] += re.compile('(@\w+)').findall(text)
            interests['hashtags'] += re.compile('(#\w+)').findall(text)

        interests['users'].sort()
        interests['hashtags'].sort()
        interests['links'].sort()
        return interests

    def twitter_locate(self, tweets, cities):
        locations = []
        locCnt = 0
        cityCnt = 0
        tweetsText = ""
        for tweet in tweets:
            if tweet['geo'] != None:
                locations.append(tweet['geo'])
                locCnt += 1
                tweetsText += tweet['tweet'].lower()
        for city in cities:
            if city in tweetsText:
                locations.append(city)
                cityCnt += 1
        print "[+] Found " + str(locCnt) + " locations via Twitter API and " + str(cityCnt) + " locations from text search."
        return locations

def main():
    parser = optparse.OptionParser('usage%prog -u <twitter handle>')
    parser.add_option('-u', dest='handle', type='string', help='specify twitter handle')
    (options, args) = parser.parse_args()
    handle = options.handle
    if handle == None:
        print parser.usage
        exit(0)
    spamTgt = ReconPerson(handle)
    tweets = spamTgt.get_tweets()
    interests = spamTgt.find_interests(tweets)
    print '\n[+] Users.'
    for user in set(interests['users']):
        print ' [+] ' + str(user)

    print '\n[+] HashTags.'
    for hashtag in set(interests['hashtags']):
        print ' [+] ' + str(hashtag)

if __name__ == '__main__':
    main()





