# -*- coding: utf-8 -*-

from os import stat;

def get_mtime (areas):
    ret = ''
    for ea in areas:
        try:
            fstat = stat('echo/%s' % ea)
            ret += ea + ':' + str(int(fstat.st_mtime)) + '\n'
        except:
            ret += ea + ':0\n'
    return ret
