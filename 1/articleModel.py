# coding=utf8
import web, datetime
import sae.const

#数据库连接  
db = web.database(dbn='mysql', db=sae.const.MYSQL_DB, user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,host=sae.const.MYSQL_HOST, port=3307) 
#获取所有文章  
def get_posts():  
    return db.select('t_entries', order = 'id DESC')  
      
#获取文章内容  
def get_post(id):  
    try:  
        return db.select('t_entries', where = 'id=$id', vars = locals())[0]  
    except IndexError:  
        return None  
#新建文章  
def new_post(title, text,html,cover):  
    db.insert('t_entries',  
        title = title,  
        content = text,  
        html = html,
        cover = cover,
        posted_on = datetime.datetime.utcnow())  
#删除文章  
def del_post(id):  
    db.delete('t_entries', where = 'id = $id', vars = locals())  
      
#修改文章  
def update_post(id, title, text,html,cover):  
    db.update('t_entries',  
        where = 'id = $id',  
        vars = locals(),  
        title = title,  
        html = html,
        cover = cover,
        content = text) 