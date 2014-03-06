import re

def echo_flt(ea):
    if re.match('^[a-z0-9_!.-]{,60}.\d{,9}$',ea): return True
