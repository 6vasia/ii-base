# -*- coding: utf-8 -*-

from bottle import *
import api, ww, api.sx as sx, api.flt as flt, points
echolist = []

NODE='test'
NODEPASS=[]

def load_echo():
    global echolist
    echoareas = open('list.txt').read().splitlines()
    echolist = [(x,api.echoarea_count(x)) for x in echoareas]
load_echo()

#@hook('before_request')
def allstart():
    ip=request.headers.get('X-Real-Ip') or request.environ.get('REMOTE_ADDR')
    local.r = sx.mydict(url='http://ii.51t.ru/',ua=request.headers.get('User-Agent'),ip=ip,kuk=sx.mydict(request.cookies),fz=sx.mydict(request.forms),getl=sx.mydict(request.GET))
    local.r.auth = local.r.kuk.auth

@route('/')
def start_redir():
    redirect(echolist[0][0])

@route('/list.txt')
def list_txt():
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join(['%s:%s:' % t for t in echolist])

@route('/<echo>.<year:int>')
def index_list(echo,year):
    allstart()
    ea = '%s.%s' % (echo,year)
    if not flt.echo_flt(ea): return ea
    local.r.page_title = u'новое фидо апреля'
    return template('start.html',r=local.r,j=api.get_echoarea(ea),ea=ea,echolist=echolist)

@post('/a/newmsg/<ea>')
def msg_post(ea):
    allstart()
    if not flt.echo_flt(ea): return ea
    if not local.r.fz.msg or not local.r.fz.subj: return 'empty msg'
    ufor = request.forms.msgfrom.encode('utf-8')
    uname, uaddr = points.check_hash(ufor or local.r.auth)
    if not uaddr: return 'no auth'
    repto = ww.find_bysubj( local.r.fz.subj.decode('utf-8')[4:], ea )
    mo = sx.mydict()
    for _ in ('subj', 'msg'):
        mo[_] = local.r.fz[_].decode('utf-8')
    mo['msgfrom'] = uname
    mo['msg']=mo['msg'].replace('\r\n','\n')
    mo.update(addr='%s,%s' % (NODE,uaddr),msgto='All',echoarea=ea)
    if repto: mo['repto']=repto
    h = ww.send_msg(mo)
    load_echo()
    redir = '/%s' % ea
    #redirect (redir)
    if ufor:
        response.set_cookie('auth',ufor,path='/',max_age=7776000)
        return ('<html><head><meta http-equiv="refresh" content="0; %s" /></head><body></body></html>' % redir)
    else:
        redirect (redir)

@route('/z/m/<h>')
def jt_outmsg(h):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.mk_jt(h,api.raw_msg(h))

@route('/z/get/<echos:path>')
#def jt_echo(auth,echos):
def jt_echo(echos):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join( [api.mk_jt(x,api.raw_msg(x)) for x in ww.parse_echos(echos)] )

@route('/z/in/<auth>/<jt>')
def jt_get(auth,jt):
    if auth and auth in NODEPASS:
        api.ins_fromjt(jt)
        load_echo()

@get('/z/in')
def jt_drawform():
    return '<form method="POST" action="/z/in"><input type="text" name="auth" /><textarea name="jt"></textarea><input type="submit" /></form>'

@post('/z/in')
def jt_post():
    allstart()
    if local.r.fz.auth and local.r.fz.auth in NODEPASS:
        for n in local.r.fz.jt.splitlines():
            api.ins_fromjt(n)
            load_echo()
            return 'uploaded'

@route('/z/push/<pauth>/<tmsg>')
def point_msg(pauth,tmsg):
    msgfrom, addr = points.check_hash(pauth)
    if not addr: return 'i che eto bilo?'
    mo = api.toss(msgfrom,addr,tmsg)
    if not mo: return 'bad echoarea or bad something else!'
    if mo.msg.startswith('@repto:'):
        tmpmsg = mo.msg.splitlines()
        mo.repto = tmpmsg[0][7:]
        mo.msg = '\n'.join(tmpmsg[1:])
        # а ещё лучше - засунуть это в api.toss
    h = ww.send_msg(mo)
    load_echo()
    redirect ('/' + mo.echoarea)

@route('/m/<msg:re:[^/]{4,}>')
def get_msg(msg):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return api.raw_msg(msg)

@route('/e/<echoarea>')
def get_echolist(echoarea):
    response.set_header ('content-type','text/plain; charset=utf-8')
    return '\n'.join(  api.get_echoarea(echoarea) )

@route('/s/<filename:path>')
def new_style(filename):
    return static_file(filename,root='./s')

@route('/q/<msglst:path>')
def msg_page(msglst):
    return template('msg.html',lst=[api.get_msg(n) + {'msgid':n} for n in msglst.split('/')])

@route('/<msghash:re:[^/]{20,}>')
def msg_page(msghash):
    return template('msg.html',lst=[api.get_msg(msghash) + {'msgid':msghash}])

run(host='127.0.0.1',port=62220,debug=False)
