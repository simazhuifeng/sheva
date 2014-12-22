# coding: utf-8
import sae
import web
import urllib 
import urllib2
import model
import datetime
from lxml import etree
from lxml import html

urls = (
      '/', 'index',
      '/weizhang','weizhang',
      '/weixin', 'weixin'
)

class index:        
    def GET(self):
        content = ''
    	url = 'http://202.99.246.243:8015/publishwcf/EnvAQIServeice.svc'
        dataTpl = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
	<s:Body>
        		<GetAllHistoryByNameAndTime xmlns="http://tempuri.org/">
                        	<PositionName>%s</PositionName>
                                <PollutantCode>PO105,PO103,PO102,PO106</PollutantCode>
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
       
class weizhang:        
    def GET(self):
        content = ''
        contentTpl = u'''\
违章时间：%s 
违章地点：%s
%s
%s
================
'''
	format0 = "%Y.%m.%d %H:%M:%S"
	format1 = u"%Y年%m月%d日 %H:%M:%S"
    	url = 'http://www.nmgat.gov.cn/search?searchword=hphm%3D%E8%92%99AAQ333+and+clsbdh%3D%25LFMJW30F290035173&perpage=100&templet=&token=&channelid=260940&hphm=%E8%92%99AAQ333&clsbdh=LFMJW30F290035173'
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'text/html; charset=utf-8')
        response = urllib2.urlopen(req)
        data = response.read()
        doc = html.document_fromstring(data)
        divs = doc.xpath("//div[@class='jj_cx_xx']") 
        for node in divs:
                timeStr = node.xpath("table/tr")[3][1].text_content().strip().split(u'：')[1]
		time = datetime.datetime.strptime(timeStr, format0)
                event = node.xpath("table/tr")[2].text_content().strip().split(u'：')[1]
                place = node.xpath("table/tr")[1].text_content().strip().split(u'：')[1]
                punisher = node.xpath("table/tr")[4][0].text_content().strip().split(u'：')[1]
                fine = node.xpath("table/tr")[4][1].text_content().strip().split(u'：')[1][1:]
                pay = "\"1\"" in node.xpath("table/tr")[5][0].text_content().strip().split(u'：')[1]
                payTimeStr = node.xpath("table/tr")[5][1].text_content().strip().split(u'：')[1]
                if pay:
                	payTime = datetime.datetime.strptime(payTimeStr, "%Y.%m.%d %H:%M:%S")
                closed = "\"1\"" in node.xpath("table/tr")[6][0].text_content().strip().split(u'：')[1]
                closedTimeStr = node.xpath("table/tr")[6][1].text_content().strip().split(u'：')[1]
                if closed:
                	closedTime = datetime.datetime.strptime(closedTimeStr, "%Y.%m.%d %H:%M:%S")
                content += contentTpl % (str(time),place,\
                u'罚款金额：' + fine + u'元' if len(fine) else '',\
                (u'【已处理】处理时间：' + payTimeStr if pay else u"【未处理】"))
	return content
       
import math

import math

class weixin:
	def GET(self):
		temp = 999999
                nearest_station = {}
                content = ''
		for station in model.get_air_station_all():
        		distance = haversine((40.848034,111.646414),(station['latitude'],station['longitude']))
                	if distance < temp:
                        	temp = distance
                                nearest_station = station
                		content += station['name'] +  str(distance)+'\n'
        	return nearest_station
def cosrad(n):
    "Return the cosine of ``n`` degrees in radians."
    return math.cos(math.radians(n))
     
def haversine((lat1, long1), (lat2, long2)):
    """Calculate the distance between two points on earth.
    """
    earth_radius = 6371  # km
    dLat = math.radians(lat2 - lat1)
    dLong = math.radians(long2 - long1)
 
    a = (math.sin(dLat / 2) ** 2 +
         cosrad(lat1) * cosrad(lat2) * math.sin(dLong / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d
app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)