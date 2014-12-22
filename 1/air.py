# coding=utf8
from datetime import *
import time
from lxml import etree
import urllib 
import urllib2
import model
import misc
import math
import json
import bike
import web


urls = (
    '/nearby', 'station_nearby',
    '/airdata', 'airdatanew',
    '/backupairdata', 'backupairdata'
)
#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#指定模板目录，并设定公共模板  
render = web.template.render('templates', base='base', globals=t_globals)  


airContentTpl = u'''



距离你最近观测站的PM2.5浓度值
******************
** %s **
(距离你%s) 
%s 时
PM2.5浓度观测值

   %s %s µg/m3

*********************
健康建议
---------------------
>>浓度(0-50) 【健康】 
>>浓度(51-100) 【中等 特别敏感的人群应该考虑减少长期或沉重的负荷
>>浓度(101-150) 【对敏感人群不健康】有心脏或肺部疾病的人、老人和小孩应该减少长期或沉重的负荷
>>浓度(151-200) 【不健康】有心脏或肺部疾病的人、老人和小孩应该避免长期或沉重的负荷。其他人也应该减少长期或沉重的负荷
>>浓度(201-300) 【非常不健康】有心脏或肺部疾病的人、老人和小孩应该避免所有户外活动。其他人也应该避免长期或沉重的负荷
>>浓度(301-500) 【危险】所有人都应该避免户外活动。有心脏或肺病的人、老人和小孩应该保持在室内，减少活动

来自环保部门公开的数据。
'''
def buildAir(recv):
    print 'buildair'
 
    nearest = get_nearest_station(recv['Location_X'],recv['Location_Y'])
    station = nearest['station']
    distance = nearest['distance']
    distanceStr = str(round(distance,1)) + u'公里'
    _data = model.get_last_observ_data_by_station(station)
    emoticon = air2emoticon(_data['pm2_5'])
    content = airContentTpl % (station['name'],distanceStr,str(_data['obtime'])[5:13],emoticon,str(_data['pm2_5']))
    print content
    return content

def get_nearest_station(Location_X,Location_Y):
	temp = 999999
	nearest_station = {}
        nearest_distance = 0
	for station in model.get_air_station_all():
		distance = misc.haversine((float(Location_X),float(Location_Y)),(station['latitude'],station['longitude']))
                #print str(distance)
		if distance < temp:
			temp = distance
			nearest_station = station
                        nearest_distance = distance
	return {'station':nearest_station,'distance':nearest_distance}
def air2emoticon(data):
	if data < 51:
			return u'/微笑'
	elif data < 101:
			return u'/抠鼻'
	elif data < 151:
			return u'/撇嘴'
	elif data < 201:
			return u'/折磨'
	elif data < 301:
			return u'/快哭了'
	elif data < 500:
			return u'/流泪'
	else :
			return u'/衰 传说中的爆表'
class backupairdata:        
    def GET(self):
        model.move_air_station()
class airdatanew:        
    def GET(self):
        print 'airdatanew'
        content = ''
        url = 'http://www.pm25.in/api/querys/all_cities.json?token=qtgiubFzTSVMhRLyQLz4'
        #url = 'http://www.pm25.in/api/querys/all_cities.json?token=qtgiubFzTSVMhRLyQLz4'
        #url = 'http://1.hushixiaodao.sinaapp.com/static/all_cities.json'
        req = urllib2.Request(url)
        print url
        response = urllib2.urlopen(req)
        data = response.read()
        root = json.loads(data)
        print data
        for station in root:
            aqi = str(station['aqi'])
            co = str(station['co'])
            co_24h = str(station['co_24h'])
            no2 = str(station['no2'])
            no2_24h = str(station['no2_24h'])
            o3 = str(station['o3'])
            o3_24h = str(station['o3_24h'])
            o3_8h = str(station['o3_8h'])
            o3_8h_24h = str(station['o3_8h_24h'])
            pm10 = str(station['pm10'])
            pm10_24h = str(station['pm10_24h'])
            pm2_5 = str(station['pm2_5'])
            pm2_5_24h = str(station['pm2_5_24h'])
            position_name = '' if station['position_name'] is None else station['position_name']
            primary_pollutant = '' if station['primary_pollutant'] is None else station['primary_pollutant']
            quality = '' if station['quality'] is None else station['quality']
            so2 = str(station['so2'])
            so2_24h = str(station['so2_24h'])
            code = str(station['station_code'])
            time_point = str(station['time_point'])
            model.new_air_data_new(code,time_point.replace('T',' ')[0:19],aqi,co,co_24h,no2,no2_24h,o3,o3_24h,o3_8h,o3_8h_24h,\
                                   pm10,pm10_24h,pm2_5,pm2_5_24h,position_name,primary_pollutant,quality,so2,so2_24h)
        return data

class station_nearby:        
    def GET(self):
        data = web.input()
        nearest = get_nearest_station(data.lat,data.lon)
        station = nearest['station']
        distance = nearest['distance']
        distanceStr = str(round(distance,1)) + u'公里'
        _data = model.get_last_observ_data_by_station(station)
        emoticon = air2emoticon(_data['pm2_5'])
        return render.air(station['name'],distanceStr,str(_data['obtime'])[5:13],emoticon,str(_data['pm2_5']))

class airdata:        
    def GET(self):
    	print 'airdata'
        content = ''
    	url = 'http://202.99.246.243:8015/publishwcf/EnvAQIServeice.svc'
        dataTpl = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
	<s:Body>
        		<GetAllHistoryByNameAndTime xmlns="http://tempuri.org/">
                        	<PositionName>%s</PositionName>
                                <PollutantCode>PO105,PO103,PO102,PO106,PO101,PO104</PollutantCode>
			</GetAllHistoryByNameAndTime>
	</s:Body>
</s:Envelope>'''
	for station in model.get_air_station_all():
                requestData = dataTpl % (station['code'])
    		req = urllib2.Request(url,requestData)
        	req.add_header('SOAPAction', 'http://tempuri.org/IEnvAQIServeice/GetAllHistoryByNameAndTime')
        	req.add_header('Content-Type', 'text/xml; charset=utf-8')
		response = urllib2.urlopen(req)
		data = response.read()
        	root = etree.fromstring( data )
        	valueRoot = root[0][0][0]
        	for elementNode in valueRoot:
        		element = elementNode[0].text
        		valuesNode = elementNode[1]
        		values = []
			for valueNode in valuesNode:
				value = {}
				for key in valueNode:
                			tag = key.tag
                                        text = key.text
                                        value[tag[tag.find('}') + 1:]] = text
                		values.append(value)
			for item in values:
        			content += '\n' + str(item['TimePoint']) + '=' + str(item['MonValue']) +  '___' + element
                        	model.new_air_data(station['code'],str(item['TimePoint']).replace('T',' ')[0:19],element,str(item['MonValue']))
	return content

app_air = web.application(urls, globals())      