# -*- coding: utf-8 -*-

import json, hashlib, base64, zlib, sx

def hsh(s):
    return base64.urlsafe_b64encode( hashlib.sha256(s).digest() ).replace('-','A').replace('_','A')[:20]

def jout(d):
    return json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '),  ensure_ascii=False)

def jl(msg):
    return json.loads( msg,object_pairs_hook=sx.mydict )

def get_msgs(msglist):
    out = []
    for h in msglist:
        msg = raw_msg(h)
        if msg: out.append( jl(msg) )
    return out

def get_msg(msgid):
    out = get_msgs([msgid])
    if out: return out[0]

def raw_msg(h):
    try:
        return open('msg/%s' % h).read().decode('utf-8')
    except:
        return ''

def raw_msgs(msglist):
    out = []
    for h in msglist:
        out.append( raw_msg(h) )
    return out

def new_msg(obj,rh=None):
    s = jout(obj).encode('utf-8')
    h = rh or hsh(s)
    open('msg/%s' % h,'wb').write(s)
    return h

def get_echoarea(name):
    try:
        return open('echo/%s' % name).read().splitlines()
    except:
        return ''

def echoarea_count(name):
    return len(get_echoarea(name))

def msg_to_echoarea(msgid,*echoarea):
    for name in echoarea:
        if name: open('echo/%s' % name,'ab').write(msgid + '\n')


def mk_jt(mh,mb):
    return mh + ':' + base64.urlsafe_b64encode( zlib.compress(mb.encode('utf-8')) )

def un_jt(txt):
    obj = txt.split(':',1)
    return (obj[0],  zlib.decompress(base64.urlsafe_b64decode(obj[1]) ).decode('utf-8') )

def ins_fromjt(n):
    (o,m) = un_jt(n)
    if not raw_msg(o):
        mo = jl(m)
        new_msg(mo,o)
        echos = [mo.echoarea] + mo.xc.split(' ')
        msg_to_echoarea(o,*echos)
    return o

def parse_jt(dta):
    for n in dta.splitlines():
        ins_fromjt(n)

def toss(msgfrom,addr,tmsg):
    lines = zlib.decompress(base64.urlsafe_b64decode(tmsg)).decode('utf-8').splitlines()
    echos = lines[0].split(' ',1)
    mo = sx.mydict(date=sx.gts(),msgfrom=msgfrom,addr=addr,echoarea=echos[0],msgto=lines[1],subj=lines[2],msg='\n'.join(lines[4:]))
    if len(echos) > 1: mo.update(xc=echos[1])
    return mo
