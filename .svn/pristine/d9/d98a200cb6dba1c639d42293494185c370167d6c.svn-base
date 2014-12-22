# coding=utf8
'''
Created on 2014-6-12

@author: sheva.wen
'''
import model
import misc
import web
import urllib2
import json
urls = (
    '/nearby', 'station_nearby'
)
#模板公共变量  
t_globals = {  
    'datestr': web.datestr,  
    'cookie': web.cookies,  
}  
#指定模板目录，并设定公共模板  
render = web.template.render('templates', base='base', globals=t_globals)  

def buildBike(recv):
    content = u'距离你最近的9个公共自行车站\n******************\n'
    baiduLonlat = get_baidu_lonlat(recv['Location_X'],recv['Location_Y'])
    lon = baiduLonlat['lon']
    lat = baiduLonlat['lat']
    content += '\n'.join('>>' + e['station']['name'] + u'（' + e['station']['address'] + u',距你' + str(e['distance']) + u'公里）' for e in get_nearby_bike_station(lon,lat,9))
    bikeLinkTpl = u'\n\n<a href="http://hushixiaodao.sinaapp.com/bike/nearby?lat=%s&lon=%s">在地图上查看这些站点</a>'
    airLinkTpl = u'\n\n\n=========\n\n<a href="http://hushixiaodao.sinaapp.com/air/nearby?lat=%s&lon=%s">是来查附近的pm2.5的？老朋友，点这里！</a>'
    content += bikeLinkTpl % (recv['Location_X'],recv['Location_Y'])
    content += airLinkTpl % (recv['Location_X'],recv['Location_Y'])

    return content
    
def get_nearby_bike_station(Location_X,Location_Y,count):
    nearby_stations = []
    print 'bike station size '  + str(len(model.get_bike_station_all()))
    for station in model.get_bike_station_all():
        distance = misc.haversine((float(Location_X),float(Location_Y)),(station['lat'],station['lon']))
        nearby_stations.append({'station':station,'distance':round(distance,1)})
    nearby_stations = sorted(nearby_stations, key=lambda station : station['distance'])           
    return nearby_stations[:count]

def get_baidu_lonlat(lon,lat):
    url = 'http://api.map.baidu.com/geoconv/v1/?from=3&coords=%s,%s&ak=729855bc6f894eaafbcc8792f74e2cc4&output=json'
    url = url % (lon,lat)
    req = urllib2.Request(url)
    print url
    response = urllib2.urlopen(req)
    data = response.read()
    root = json.loads(data)
    # {"status":0,"result":[{"x":114.22539195429,"y":29.581585367458}]}
    lon = root['result'][0]['x']
    lat = root['result'][0]['y']
    return {'lon':lon,'lat':lat}
class station_nearby:        
    def GET(self):
        data = web.input()
        baiduLonlat = get_baidu_lonlat(data.lon,data.lat)
        lon = baiduLonlat['lon']
        lat = baiduLonlat['lat']
        
        stations = get_nearby_bike_station(lat,lon,9)
        stationstr = '|'.join(str(e['station']['lon']) + ',' + str(e['station']['lat']) for e in stations)
        markerStyles = '|'.join('l,' + str(e)  for e in range(1,len(stations) + 1))
        return render.bike(lon,lat,stationstr,markerStyles,stations)

app_bike = web.application(urls, globals())      