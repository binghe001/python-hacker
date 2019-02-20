#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: gbk -*-
# Date: 2019/2/19
# Created by 冰河
# Description 复制RadioTap、802.11、SNAP、LLC、IP和UDP层中的信息
#             命令行进入scapy命令，输入ls(Dot11)即可查看信息：
#             C:\Users\liuyazhuang>scapy
#             >>> ls(Dot11)
#             subtype    : BitField (4 bits)                   = (0)
#             type       : BitEnumField (2 bits)               = (0)
#             proto      : BitField (2 bits)                   = (0)
#             FCfield    : FlagsField (8 bits)                 = (<Flag 0 ()>)
#             ID         : ShortField                          = (0)
#             addr1      : MACField                            = ('00:00:00:00:00:00')
#             addr2      : MACField (Cond)                     = ('00:00:00:00:00:00')
#             addr3      : MACField (Cond)                     = ('00:00:00:00:00:00')
#             SC         : LEShortField (Cond)                 = (0)
#             addr4      : MACField (Cond)                     = ('00:00:00:00:00:00')
#
# 博客 https://blog.csdn.net/l1028386804

from scapy.all import *

def dupRadio(pkt):
    rPkt = pkt.getlayer(RadioTap)
    version = rPkt.version
    pad = rPkt.pad
    present = rPkt.present
    notdecoded = rPkt.notdecoded
    nPkt = RadioTap(version=version, pad=pad, present=present, notdecoded=notdecoded)
    return nPkt


def dupDot11(pkt):
    dPkt.subtype
    subtype = dPkt.subtype
    Type = dPkt.type
    proto = dPkt.proto
    FCfield = dPkt.FCfield
    ID = dPkt.ID
    addr1 = dPkt.addr1
    addr2 = dPkt.addr2
    addr3 = dPkt.addr3
    SC = dPkt.SC
    addr4 = dPkt.addr4
    nPkt = Dot11(subtype=subtype, type=Type, proto=proto, FCfield=dr4)
    return nPkt

def dupSNAP(pkt):
    sPkt = pkt.getlayer(SNAP)
    oui = sPkt.OUI
    code = sPkt.code
    nPkt = SNAP(OUI=oui, code=code)
    return nPkt


def dupLLC(pkt):
    lPkt = pkt.getlayer(LLC)
    dsap = lPkt.dsap
    ssap = lPkt.ssap
    ctrl = lPkt.ctrl
    nPkt = LLC(dsap=dsap, ssap=ssap, ctrl=ctrl)
    return nPkt

def dupIP(pkt):
    iPkt = pkt.getlayer(IP)
    version = iPkt.version
    tos = iPkt.tos
    ID = iPkt.id
    flags = iPkt.flags
    ttl = iPkt.ttl
    proto = iPkt.proto
    src = iPkt.src
    dst = iPkt.dst
    options = iPkt.options
    nPkt = IP(version=version, id=ID, tos=tos, flags=flags,ttl=ttl, proto=proto, src=src, dst=dst,options=options)
    return nPkt


def dupUDP(pkt):
    uPkt = pkt.getlayer(UDP)
    sport = uPkt.sport
    dport = uPkt.dport
    nPkt = UDP(sport=sport, dport=dport)
    return nPkt
