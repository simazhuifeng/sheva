# coding=utf8
import os

import sae
import sae.const
import web
import os
import hashlib
import model
import misc
import router
from datetime import *
from lxml import etree
from lxml import html
import urllib 
import urllib2
import os
import bike
import air
import article
import weizhang
import event
from web import form
from sae.ext.shell import ShellMiddleware
import socket
import json

urls = (
	"/", 'index',
	"/article", article.app_article,
	"/bike", bike.app_bike,
	"/air", air.app_air,
	"/event", event.app_event,
	'/weixin', 'weixin',
	'/ipproxy', 'ipproxy',
	'/ipcheck', 'ipcheck',
	'/jiankong_fetch', 'jiankong_fetch',
	'/jiankong', 'jiankong',
	'/jiankong_search', 'jiankong_search',
	'/getcode', 'getcode',
	'/dialog', 'dialog',
	'/ping', 'ping',
	'/weizhangdata', 'weizhangdata',
	'/weizhang', 'weizhangtest',
	'/gwy', 'gwy',
    '/report', 'report',
    '/whereareyou','whereareyou'
)
#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#指定模板目录，并设定公共模板  
render = web.template.render('templates', base='base', globals=t_globals) 

#TOKEN
config={"TOKEN":'hushixiaodao',
	"WEIXIN": 'weixin'}
        
app_root = os.path.dirname(__file__)

class index:        
	def GET(self):
		i = web.input(name=None)
		return render.hello()
class report:        
    def GET(self):
        i = web.input()
        return 'ok'
class dialog:        
	def GET(self):
		dialogs = model.conversation_all()
		return render.dialog(dialogs)
class weixin:
    #GET register url
    def GET(self):
        data = web.input()
        #
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr

        #
        token = config['TOKEN']
        
        #
        tmplist = [ token, timestamp, nonce ]
        tmplist.sort()
        tmplist.sort()
        tmpstr = ''.join( tmplist )
        hashstr = hashlib.sha1( tmpstr ).hexdigest()

        #
        if hashstr == signature:
            return echostr
        
        #
        print signature,timestamp,nonce
        print tmpstr,hashstr
        return 'Error' + echostr


    def POST(self):
    	ISOTIMEFORMAT='%Y-%m-%d %X'
        #
        data = web.data()
        print data
        recv = misc.xml2obj(data)
        #print data
        #print recv
        
        #
        model.new_conversation(data,recv['FromUserName'],'me', datetime.now().strftime(ISOTIMEFORMAT))
        textTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <Content><![CDATA[%s]]></Content>
            <FuncFlag>0</FuncFlag>
            </xml>"""
        articleTpl = """<xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[%s]]></MsgType>
            <ArticleCount>%s</ArticleCount>
            <Articles>
            %s
            </Articles>
            </xml> """
        itemTpl = """<item>
            <Title><![CDATA[%s]]></Title> 
            <Description><![CDATA[%s]]></Description>
            <PicUrl><![CDATA[%s]]></PicUrl>
            <Url><![CDATA[%s]]></Url>
            </item>"""
        content = router.route(recv)
        echostr = ""
        itemstr = ""
        print content
        if(content.startswith("article$$")):
            items = content.split("$$")
            for item in items:
                fields = item.split("|")
                if(len(fields) == 4):
                    if("?" in fields[2]):
                        fields[2] += "&"
                    else:
                        fields[2] += "?"
                    fields[2] += "open_id=" + recv['FromUserName']
                    itemstr += itemTpl % (fields[0],fields[1],fields[3],fields[2])
            echostr = articleTpl % (recv['FromUserName'], recv['ToUserName'],str(datetime.now().microsecond),'news',len(items) - 1,itemstr)
        else:
            echostr = textTpl % (recv['FromUserName'], recv['ToUserName'],str(datetime.now().microsecond),'text',content)
        #print echostr
        model.new_conversation(echostr,'me',recv['FromUserName'], datetime.now().strftime(ISOTIMEFORMAT))
	return echostr


ipproxy_form = form.Form(
	form.Textarea("ip", description="ip address"),
	form.Button("submit", type="submit", description="submit")
)
class jiankong_fetch:
	def GET(self):
		data = web.input()
		pre = int(data.pre) if hasattr(data, 'pre') else 2
		return weizhang.getJiankong(datetime.now() - timedelta(days=pre))
class jiankong:
	def GET(self):
		data = web.input()
		chepai = data.chepai if hasattr(data, 'chepai') else u'蒙AAQ333'
		return render.jiankong(model.get_jiankong(chepai))
class jiankong_search:
	def GET(self):
		return render.jiankong_search()
class ipcheck:
	def GET(self):
		weizhang.ipcheck()
class weizhangtest:
	def GET(self):
		data = web.input()
		weizhang._search(u'蒙ABP779','315864')
class getcode:
	def GET(self):
		weizhang.getcode()
class ping:
	def GET(self):
		data = web.input()
                model.misc_set('weizhang_open',misc.url_ping(data.url))

class weizhangdata:
	def GET(self):
		datas = model.weizhangdata()
		return render.weizhangdata(datas)
gwy_form = form.Form(
	form.Textbox("zhuanye", description="关键字"),
	form.Button("ok", type="submit", description="过滤")
)

class gwy:
	def GET(self):
		f = gwy_form()
		params = web.input()
		page = params.page if hasattr(params, 'page') else 1
		perpage = 100
		offset = (int(page) - 1) * perpage
		datas = model.gwydata(offset,perpage,"")
		pages = 3500 / perpage
		return render.gwy(datas,pages=pages,form=f)
	def POST(self):
		f = gwy_form()
		if f.validates():
			user_data = web.input()
			datas = model.gwydata(0,300,user_data.zhuanye)
			return render.gwy(datas,pages=1,form=f)
class ipproxy:
	def GET(self):
		f = ipproxy_form()
		table = model.ipaddress_all()
		return render.ipproxy(table,f)
	def POST(self):
        	f = ipproxy_form()
        	if not f.validates():
                	table = model.ipaddress_all()
			return render.ipproxy(table,f)
		else:
                	user_data = web.input()
                        ips = user_data.ip.split('\r\n')
                        model.ipaddress_remove_all()
                        last_ip = ''
                        for i in range(0,len(ips)):
                            if(last_ip != ips[i].split(':')[0]):
                                model.ipaddress_insert(ips[i])
                                last_ip = ips[i].split(':')[0]
                            table = model.ipaddress_all()
                        return render.ipproxy(table,f)


import ocr
from StringIO import StringIO
def getrandcode():
    response = urllib2.urlopen('http://jjzd.nmgat.gov.cn/VerifyCodeServlet?timestamp=' + str(int(time.time())))
    imgdata = response.read()
    print response.info().getheader('Set-Cookie')
    return imgdata


app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(ShellMiddleware(app))