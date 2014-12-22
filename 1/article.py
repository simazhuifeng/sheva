# coding=utf8
import web   
import articleModel
from os import listdir
from os.path import isfile, join
import json


urls = (
	'/', 'Index',  
	'/view/(.+)', 'View',  
	'/new', 'New',  
    '/list', 'List', 
	'/delete/(.+)', 'Delete',  
	'/edit/(.+)', 'Edit',  
	'/login', 'Login',  
	'/logout', 'Logout'
)
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

#首页类  
class Index:  
    def GET(self):  
        login_form = login()  
        posts = articleModel.get_posts()  
        return render.index(posts, login_form)  
    def POST(self):  
        login_form = login()  
        if login_form.validates():  
            if login_form.d.username == 'admin' and login_form.d.password == 'symantec':  
                web.setcookie('username', login_form.d.username)  
        raise web.seeother('/')
#查看文章类  
class View:  
    def GET(self, id):  
        post = articleModel.get_post(int(id))
        return render.view(post)  
#新建文章类  
class New:  
    form = web.form.Form(  
	web.form.Textbox('title',  
	web.form.notnull,  
	size=30,  
	description='Post title: '),  
	web.form.Textarea('content',  
		web.form.notnull,  
		rows=30,  
		cols=80,  
		description='Post content: '
        ), 
    web.form.Hidden('html'),
    web.form.Hidden('cover'),
	web.form.Button('Post entry')
    )  
    def GET(self):  
        form = self.form()  
        mypath = "static"
        files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and any(f.endswith(x) for x in ('.jpg','.gif','.png')) ]
        return render.new(form,files)  
    def POST(self):  
        form = self.form()  
        if not form.validates():  
            return render.new(form)  
        articleModel.new_post(form.d.title, form.d.content,form.d.html,form.d.cover)  
        raise web.seeother('/')  
#删除文章类  
class Delete:  
    def POST(self, id):  
        articleModel.del_post(int(id))  
        raise web.seeother('/')  
#编辑文章类  
class Edit:  
    def GET(self, id):  
        post = articleModel.get_post(int(id))  
        form = New.form()  
        form.fill(post)  
        mypath = "static"
        files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and any(f.endswith(x) for x in ('.jpg','.gif','.png')) ]
        return render.edit(post, form,files)  
    def POST(self, id):  
        form = New.form()  
        post = articleModel.get_post(int(id))  
        if not form.validates():  
            return render.edit(post, form)  
        articleModel.update_post(int(id), form.d.title, form.d.content,form.d.html,form.d.cover)  
        raise web.seeother('/')  
#JSON  
class List:  
    def GET(self):   
        posts = list(articleModel.get_posts())
        print 'posts length:' + str(len(posts))
        for post in posts:
            post.posted_on = str(post.posted_on)
            post.html = ""
            post.content = ""
        print 'list length:' + str(len(list(posts)))
        return json.dumps(posts)
#退出登录  
class Logout:  
    def GET(self):  
        web.setcookie('username', '', expires=-1)  
        raise web.seeother('/') 
        

app_article = web.application(urls, globals())