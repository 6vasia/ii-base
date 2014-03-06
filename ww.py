# -*- coding: utf-8 -*-

import api, api.sx as sx, os

def send_msg(tags):
    mo = sx.mydict(date=sx.gts())
    mo.update(**tags)
    h = api.new_msg(mo)
    to = [tags.echoarea] + tags.xc.split(' ')
    api.msg_to_echoarea(h,*to)
    return h

def qua(ea,s):
    items =  api.get_echoarea(ea)
    if len(s) < 6 and s.isdigit():
        return items[-int(s):]
    else:
        pool = []
        for n in reversed(items):
            if n == s: break
            pool.insert(0,n)
        return pool

def parse_echos(el):
    echos = el.split('/')
    pool = []
    for ea in echos:
        if ':' in ea:
            items = qua(*ea.split(':',1))
        else:
            items = api.get_echoarea(ea)
        for x in items:
            if not x in pool:
                pool.append(x)
    return pool

def find_bysubj(subj,ea):
    for x in api.get_echoarea(ea):
        mo = api.get_msg(x)
        if not mo.repto and mo.subj == subj:
            return x
