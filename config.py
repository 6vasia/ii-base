# -*- coding: utf-8 -*-

import re
import sys

def config(filename):
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
        return ret
    except:
        print sys.exc_info()
        return None
