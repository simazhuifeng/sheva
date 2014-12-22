import web, datetime
import sae.const

db = web.database(dbn='mysql', db=sae.const.MYSQL_DB, user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,host=sae.const.MYSQL_HOST, port=3307) 
def get_item(text):
    try:
            nickname = db.select('t_nickname', where="name like $text", vars=dict(text=text +'%'))[0]
            itemid = nickname['itemid']
            return db.select('t_item', where="itemid=$itemid",vars=locals())[0]
    except IndexError:
            return None

def get_item_all():
	return list(db.select('t_item'))

def get_nickname_all():
	return list(db.select('t_nickname'))
        
def get_event(itemid):
    try:
            return db.query("SELECT * FROM t_event where itemid=$itemid and available=true order by time desc",vars=locals())[0]
    except IndexError:
            return None

def get_event_all():
	items = get_item_all()
        for item in items:
        	event = get_event(item['itemid'])
                #print item
                if event:
                	item['event'] = event
                        #print item
        return items
def new_event(itemid, content,commit,time,available):
	db.insert('t_event', itemid=itemid, content=content, time=time,available=available,commit=commit)
    
def get_air_data_by_code_time(code,obtime):
	try:
        	#print "SELECT * FROM t_air_data where code = '" + code + "' and obtime='" + obtime + " '"
		return db.query("SELECT * FROM t_air_data where code = '" + code + "' and obtime='" + obtime + " '")[0]
	except IndexError:
		return None
def new_air_data(code,obtime,element,value):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	if get_air_data_by_code_time(code,obtime):
        	print "UPDATE t_air_data SET " + element + " = '" + value + "' WHERE code = '" + code + "' and obtime='" + obtime + " '"
        	cursor.execute("UPDATE t_air_data SET " + element + " = '" + value + "' WHERE code = '" + code + "' and obtime='" + obtime + " '") 
	else:
        	print "INSERT INTO t_air_data (code, obtime," + element + ") VALUES ('" + code + "', '" + obtime + " ','" + value + "')"
		cursor.execute("INSERT INTO t_air_data (code, obtime," + element + ") VALUES ('" + code + "', '" + obtime + " ','" + value + "')") 
	cursor.close()
def get_air_station_all():
	return list(db.select('t_air_station'))