# coding: utf-8
import model
import web
from datetime import datetime
urls = (
	'/nickname/(.+)', 'nickname',
	'/nickname', 'nickname',
	'/event/(.+)', 'event',
	'/event', 'event',
	'/item', 'item'
)
#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#指定模板目录，并设定公共模板  
render = web.template.render('templates', base='base', globals=t_globals)  
#创建登录表单  
login = web.form.Form(  
                      web.form.Textbox('username'),  
                      web.form.Password('password'),  
                      web.form.Button('login')  
                      )  
 
class event:  
    form = web.form.Form(  
	web.form.Textarea('content'), 
	web.form.Textbox('itemid'),
	web.form.Button('add')
    )  
    def GET(self,itemid):  
        form = self.form()
        event = model.get_event(itemid) 
        form.get('itemid').value = itemid
        return render.event(event,form)
    def POST(self):  
        i = web.input()
        model.new_event(i.itemid, i.content,u'...',datetime.now(),1)
        raise web.seeother('/item')
class nickname:  
    form = web.form.Form(  
	web.form.Textbox('name'), 
	web.form.Textbox('itemid'),
	web.form.Button('add')
    )  
    def GET(self,itemid):  
        form = self.form()
        names = model.get_nickname(itemid) 
        form.get('itemid').value = itemid
        return render.nickname(names,form)
    def POST(self):  
        i = web.input()
        model.new_nick(i.itemid, i.name)  
        raise web.seeother('/item')  
class item:    
    form = web.form.Form(  
	web.form.Textbox('name'), 
	web.form.Button('add')
    )  
    def GET(self):  
        form = self.form()
        items = model.get_item_all() 
        return render.item(items,form)
    def POST(self):  
        i = web.input()
        model.new_item_link_nickname(i.name)
        raise web.seeother('/item')
app_event = web.application(urls, globals())