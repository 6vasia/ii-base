# -*- coding: utf-8 -*-

import api, api.sx as sx, os

def send_msg(tags):
    mo = sx.mydict(date=sx.gts())
    mo.update(**tags)
    if api.echo_flt(tags.echoarea):
        h = api.new_msg(mo)
        api.msg_to_echoarea(h,tags.echoarea)
        return h

def qua(ea,s):
    items =  api.get_echoarea(ea)
    if len(s) < 6 and s.isdigit():
        return items[-int(s):]
    else:
        if not s in items: return items
        return items[items.index(s)+1:]

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
