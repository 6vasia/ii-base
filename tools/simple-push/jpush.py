# -*- coding: utf-8 -*-

import urllib,sys

def getf(l):
    print 'fetch %s' % l
    return urllib.urlopen(l).read()

website = 'http://ii.51t.ru/z/push'
user = '51t'
addr = '1,1'

for ea in sys.argv[1:]:
    txt = open(ea).read()
    out = getf('%s/%s:%s/%s' % (website, user,addr, txt))
