# -*- coding: utf-8 -*-

import re
import sys

_cfg = {}

def config(filename):
    if (_cfg.get(filename)):
        return _cfg[filename]
    try:
        ret = {}
        dic = {}
        section = ''
        rsect = re.compile(r'^\s*\[(\S+)\]\s*$')
        rkeyval = re.compile(r'^(\S+)\s*=\s*(.*)$')
        cfg = open(filename).readlines()
        for x in cfg:
            x = x.strip()
            smatch = rsect.match(x)
            if smatch:
                if (section and dic):
                    ret[section] = dic
                    dic = {}
                section = smatch.group(1)
            else:
                kvmatch = rkeyval.match(x)
                if (kvmatch):
                    dic[kvmatch.group(1)] = kvmatch.group(2)
        if (section and dic):
            ret[section] = dic
        _cfg[filename] = ret
        return ret
    except IOError:
        return None
