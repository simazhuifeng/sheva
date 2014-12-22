# coding=utf8
import web
import sae.const
from datetime import datetime,date, timedelta

db = web.database(dbn='mysql', db=sae.const.MYSQL_DB, user=sae.const.MYSQL_USER, pw=sae.const.MYSQL_PASS,host=sae.const.MYSQL_HOST, port=3307) 
def get_item_by_text(text):
	sql = u"SELECT DISTINCT t_item.itemid,t_item.name FROM t_nickname,t_item,t_item_nickname where  t_nickname.id = t_item_nickname.nicknameid AND t_item_nickname.itemid = t_item.itemid AND t_nickname.name LIKE '" + text + "%'"
	items = list(db.query(sql))
	return items

def get_item_by_type(_type):
	return list(db.select('t_item', where='type='+str(_type)))
def get_item_all():
	return list(db.select('t_item'))

def get_nickname_all():
	return list(db.select('t_nickname'))
def get_nickname(itemId):
	return list(db.query('SELECT `t_nickname`.* FROM `t_nickname`,t_item_nickname,t_item \
        where t_nickname.id = t_item_nickname.nicknameid and t_item.itemid = t_item_nickname.itemid and t_item.itemid = ' + itemId))

def new_nick(itemid, name):
	nicknameid = db.insert('t_nickname', name=name)
	db.insert('t_item_nickname', itemid=itemid,nicknameid=nicknameid)
def new_item_link_nickname(name):
	itemid = db.insert('t_item', name=name)
	nicknameid = db.insert('t_nickname', name=name)
	db.insert('t_item_nickname', itemid=itemid,nicknameid=nicknameid)

def get_event(itemid):
	try:
		return db.query("SELECT * FROM t_event where itemid=$itemid and available=true order by time desc",vars=locals())[0]
	except IndexError:
		return None

def get_event_all(_type):
	items = get_item_by_type(_type)
	for item in items:
		event = get_event(item['itemid'])
		if event:
			item['event'] = event
	return items
def new_event(itemid, content,commit,time,available):
	db.insert('t_event', itemid=itemid, content=content, time=time,available=available,commit=commit)
def get_air_data_by_code_time(code,obtime):
	try:
		return db.query("SELECT * FROM t_air_data where code = '" + code + "' and obtime='" + obtime + " '")[0]
	except IndexError:
		return None
def new_air_data(code,obtime,element,value):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	if get_air_data_by_code_time(code,obtime):
		cursor.execute("UPDATE t_air_data SET " + element + " = '" + value + "' WHERE code = '" + code + "' and obtime='" + obtime + " '") 
	else:
		cursor.execute("INSERT INTO t_air_data (code, obtime," + element + ") VALUES ('" + code + "', '" + obtime + " ','" + value + "')") 
	cursor.close()
def new_air_data_new(code,obtime,aqi,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,\
		pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("INSERT INTO t_air_data_new (code,obtime,aqi,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,\
		pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h) \
		VALUES ('" + code + "', '" + obtime + "','" + aqi + "', '" +co+ "', '" +co_24h+ "', '" +no2+ "', '" +no2_24h+ "', '" +o3+ "', '" +o3_24h+ "', '" +o3_8h+ "', '" +o3_8h_24h+ "', '" \
		+ pm10+ "', '" +pm10_24h+ "', '" +pm2_5+ "', '" +pm2_5_24h+ "', '" +position_name+ "', '" +primary_pollutant+ "', '" +quality+ "', '" +so2+ "', '" + so2_24h + "')") 
# 	print "INSERT INTO t_air_data_new (code,obtime,aqi,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,\
# 		pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h) \
# 		VALUES ('" + code + "', '" + obtime + "','" + aqi + "', '" +co+ "', '" +co_24h+ "', '" +no2+ "', '" +no2_24h+ "', '" +o3+ "', '" +o3_24h+ "', '" +o3_8h+ "', '" +o3_8h_24h+ "', '" \
# 		+ pm10+ "', '" +pm10_24h+ "', '" +pm2_5+ "', '" +pm2_5_24h+ "', '" + position_name + "', '" +primary_pollutant+ "', '" +quality+ "', '" +so2+ "', '" + so2_24h + "')"
	cursor.close()
def move_air_station():
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	yesterday = date.today() - timedelta(1)
	tmp = yesterday.strftime('%Y-%m-%d')
	cursor.execute("INSERT INTO t_air_data_backup SELECT * FROM t_air_data WHERE `obtime` < '" + tmp +"'")
	cursor.execute("delete from t_air_data WHERE `obtime` < '" + tmp +"'")
	cursor.close()
	print 'air data backup ' + tmp
def get_air_station_all():
	return list(db.select('t_air_station'))
def get_bike_station_all():
	return list(db.select('t_bike_station', where="lon>0"))

def get_last_observ_data_by_station(station):
	try:
		print "SELECT * FROM t_air_data_new where code='" + station['code'] + "' and aqi > 0 order by id desc limit 0, 1"
		_data = db.query("SELECT * FROM t_air_data_new where code='" + station['code'] + "' and aqi > 0 order by id desc limit 0, 1")[0]
		return _data
	except IndexError:
		return None
def new_weizhang(html):
	db.insert('t_weizhang_data', data=html,searchtime=datetime.now())
def weizhangdata():
	return list(db.select('t_weizhang_data',order="id DESC",limit=5))
def gwydata(offset,perpage,keywords):
# 	print offset
# 	print perpage
# 	print keywords
	if keywords != "":
		print "SELECT * FROM t_gwy where zhuanye like '%" + keywords + "%' or danwei like '%" + keywords + "%' order by danwei limit " + str(offset) + "," + str(perpage)
		_data = db.query("SELECT * FROM t_gwy where zhuanye like '%" + keywords + "%' or xueli like '%" + keywords + "%' or xuewei like '%" + keywords + "%' or gangwei like '%" + keywords + "%' or danwei like '%" + keywords + "%' or qita like '%" + keywords + "%' order by danwei limit " + str(offset) + "," + str(perpage))
	else:
		_data = db.where('t_gwy',order="danwei",limit=perpage,offset=offset)
	return list(_data)
def new_randcode(code,cookie):
	db.insert('t_weizhang_randcode', code=code,cookie=cookie,gettime=datetime.now(),used=0)
def last_randcode():
	try:
		return db.select('t_weizhang_randcode',where='used = 0',order='gettime DESC')[0]
	except IndexError:
		return None

def randcode_used(id):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("update t_weizhang_randcode set used = 1 where id = " + str(id))
	cursor.close()

def new_plate_number(number,engineId):
	db.insert('t_plate_number', number=number,engineId=engineId)

def plate_number(number):
	try:
		return db.select('t_plate_number',where='number=\'' + number + '\'')[0]
	except IndexError:
		return None
def new_conversation(content,fromu,tou,time):
	db.insert('t_conversation', content=content, fromu=fromu, tou=tou,time=time)
		
def conversation_all():
	records = db.select('t_conversation',order="id DESC", limit=30)
	return list(records)
def last_conversation(openid):
	print db.select('t_conversation', where='fromu=\''+openid + '\'', order="id DESC", limit=2,_test=True)
	records = db.select('t_conversation', where='fromu=\''+openid + '\'', order="id DESC", limit=2)
	if len(records) > 1:
		return records[1]
	return None
def get_ipaddress_all():
	return list(db.select('t_ip_address'))
def get_ipaddress_unchecked():
	print 'unchecked.'
	print db.select('t_ip_address', limit=5,where='checked=0',_test=True)
	return list(db.select('t_ip_address', limit=5,where='checked=0'))
def get_a_ipaddress_available():
	try:
		return db.select('t_ip_address',where='usedtimes < 5')[0]
	except IndexError:
		return None
def ipaddress_all():
	return list(db.select('t_ip_address'))
def ipaddress_checked(id):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("update t_ip_address set checked = 1 where id = " + str(id))
	cursor.close()
def ipaddress_used(id):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("update t_ip_address set usedtimes = usedtimes + 1 where id = " + str(id))
	cursor.close()
def ipaddress_remove(id):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("delete from  t_ip_address where id = " + str(id))
	cursor.close()
def ipaddress_remove_all():
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	cursor.execute("delete from t_ip_address")
	cursor.close()
def ipaddress_insert(ipaddress):
	records = db.select('t_ip_address', where='address=\''+ipaddress + '\'')
	if len(records) == 0:
		conn = db._db_cursor().connection
		cursor = conn.cursor()
		cursor.execute("insert into t_ip_address (address,usedtimes,checked) values ('" + ipaddress + "',0,0)")
		cursor.close()
def misc_set(key,value):
	conn = db._db_cursor().connection
	cursor = conn.cursor()
	print "update t_misc set _value = '" + str(value) + "' where _key = '" + key + "'"
	cursor.execute("update t_misc set _value = '" + str(value) + "' where _key = '" + key + "'")
	cursor.close()
def misc_get(key):
    try:
        return db.select('t_misc',where='_key = \'' + key + '\'')[0]['_value']
    except IndexError:
        return None
def get_air_request():
	return db.select('t_conversation',where='content like \'%Location%\' ')
def new_jiankong(chepai,text,wzdate):
	db.insert('t_jiankong', chepai=chepai, weizhang=text, wzdate=wzdate)
def get_jiankong(chepai):
	return list(db.select('t_jiankong', where="chepai=\'" + chepai + "\'",order="wzdate DESC"))