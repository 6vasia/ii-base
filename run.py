# -*- coding: utf-8 -*-

import api,points
import api.x
from api.bottle import *

II_PATH=os.path.dirname(__file__) or '.'
TEMPLATE_PATH.insert(0,II_PATH)
CONFIG='server.cfg'
api.CONFIG = CONFIG


@route('/list.txt')
def list_txt():
    response.set_header ('content-type','text/plain; charset=utf-8')
    return 'deprecated'

@route('/blacklist.txt')
def blacklist_txt():
    response.set_header ('content-type','text/plain; charset=utf-8')
    return 'deprecated'

@route('/u/m/<h:path>')
def jt_outmsg(h):
    response.set_header ('content-type','text/plain; charset=utf-8')
    lst = [x for x in h.split('/') if len(x) == 20]
    return '\n'.join( [api.mk_jt(x,api.raw_msg(x)) for x in lst] )

@route('/u/e/<names:path>')
def index_list(names):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.echoareas(names.split('/'))

def _point_msg(pauth,tmsg):
    msgfrom, addr = points.check_hash(pauth)
    if not addr: return 'auth error!'
    cfg = config('_server.cfg')
    mo = api.toss(msgfrom,'%s,%s' % (cfg['server']['address'],addr),tmsg.strip())
    if mo.msg.startswith('@repto:'):
        tmpmsg = mo.msg.splitlines()
        mo.repto = tmpmsg[0][7:]
        mo.msg = '\n'.join(tmpmsg[1:])
        # а ещё лучше - засунуть это в api.toss
    if len(mo.msg.encode('utf-8')) < 64100:
        h = api.point_newmsg(mo)
        if h:
            return 'msg ok:%s: <a href="/%s">%s</a>' % (h, mo.echoarea, mo.echoarea)
        else:
            return 'error:unknown'
    else:
        return 'msg big!'

@route('/u/point/<pauth>/<tmsg:path>')
def point_msg_get(pauth,tmsg):
    return _point_msg(pauth,tmsg)

@post('/u/point')
def point_msg_get():
    return _point_msg(request.POST['pauth'],request.POST['tmsg'])

@route('/m/<msg>')
def get_msg(msg):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.raw_msg(msg)

@route('/e/<echoarea>')
def get_echolist(echoarea):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.get_echoarea(echoarea,True)

# === extended API ===

@route('/x/t/<echoareas:path>')
def get_mtime(echoareas):
    response.set_header ('content-type','text/plain; charset=utf-8')
    arealist = echoareas.split('+')
    arealist_legacy = echoareas.split('/')
    if len(arealist) > len(arealist_legacy):
        return api.x.get_mtime(arealist)
    else:
        return api.x.get_mtime(arealist_legacy)

import iitpl
iitpl.II_PATH=II_PATH
iitpl.CONFIG = CONFIG

run(host='127.0.0.1',port=62220,debug=False)
