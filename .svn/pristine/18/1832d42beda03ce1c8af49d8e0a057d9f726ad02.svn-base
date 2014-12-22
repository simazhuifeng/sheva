# coding: utf8
'''
Created on 2013-6-8

@author: xtgl
'''
import urllib2
import urllib 
import httplib
import ocr
import socket
from lxml import html
from StringIO import StringIO
import os
import model
import math
import datetime
import time
import re

def search(plateNumber,engineNumber):
    content = ''
    contentTpl = u'''\
====== %s ======
违章时间：%s 
违章地点：%s
%s
罚款金额：%s 【%s】
罚分：%s
'''
    os.environ['disable_fetchurl'] = "1"
    code = model.last_randcode()
    model.randcode_used(code['id'])
    ipAddress = model.get_a_ipaddress_available()
    print 'use ip' + ipAddress['address']
    model.ipaddress_used(ipAddress['id'])
    proxy_support = urllib2.ProxyHandler({'http':'http://' + ipAddress['address']})
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    opener.addheaders.append(('Accept', 'text/html, application/xhtml+xml, */*'))
    opener.addheaders.append(('Referer', 'http://jjzd.nmgat.gov.cn/Query.jsp'))
    opener.addheaders.append(('Accept-Language', 'zh-CN'))
    opener.addheaders.append(('User-Agent','Mozilla/5.0 (compatible; MSIE 9.0; qdesk 2.5.1277.202; Windows NT 6.2; WOW64; Trident/6.0; MALCJS)'))
    opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
    opener.addheaders.append(('Connection', 'Keep-Alive'))
    opener.addheaders.append(('Host', 'jjzd.nmgat.gov.cn'))
    opener.addheaders.append(('Cookie', code['cookie']))
    print code['cookie']
    try:
        print "http://jjzd.nmgat.gov.cn/QueryOne.jsp?fdjh=" + engineNumber + '&' +  urllib.urlencode({'hphm':plateNumber.encode('utf8')}) + "&wfhpzl=02&RANDOM1=" + code['code']
        f = opener.open("http://jjzd.nmgat.gov.cn/QueryOne.jsp?fdjh=" + engineNumber + '&' +  urllib.urlencode({'hphm':plateNumber.encode('utf8')}) + "&wfhpzl=02&RANDOM1=" + code['code'])
        data = f.read()
    except socket.timeout:
        print 'socket.timeout '
        content = u'小道努力查了，但...复制你的车牌号再试一次吧'
        model.ipaddress_remove(ipAddress['id'])
        return content
    except urllib2.HTTPError, err:
        print 'urllib2.HTTPError ' + str(err.code)
        #if err.code == 503:
        content = u'小道努力查了，但...复制你的车牌号再试一次吧'
        model.ipaddress_remove(ipAddress['id'])
        return content
    except urllib2.URLError, err:
        print 'urllib2.URLError '
        content = u'小道努力查了，但...复制你的车牌号再试一次吧'
        model.ipaddress_remove(ipAddress['id'])
        return content
    except:
        content = u'小道努力查了，但...复制你的车牌号再试一次吧'
        model.ipaddress_remove(ipAddress['id'])
        return content        
    model.new_weizhang(data)
    if u'未找到对应车牌'.encode('utf8') in  data:
        content = u'填错了吧，请检查一下，复制你的车牌号再试一次吧'
        return content
    doc = html.document_fromstring(data)
    print data
    if(len(doc.xpath("//div[@id='SHOWMESSAGE2']")) < 1):
        print 'div[@id=SHOWMESSAGE2] < 1 '
        content = u'小道努力查了，但...复制你的车牌号再试一次吧'
        return content
    tds = doc.xpath("//div[@id='SHOWMESSAGE2']")[0].xpath("//td")
    if len(tds) > 6:
            count = (len(tds)/6)
            print 'tds count ' + str(count)
            for r in range(1,count):
                time1 = tds[r * 6 + 0].text_content()
                if len(time1) == 1:
                    break
                event = tds[r * 6 + 1].text_content()
                place = tds[r * 6 + 2].text_content()
                fine = tds[r * 6 + 3].text_content()
                payed = tds[r * 6 + 4].text_content()
                points  = tds[r * 6 + 5].text_content()
                content += contentTpl % (r,time1,place,event,fine,payed,points)
            if content == '':
                content = u'暂无违章哦'
    else:
        content = u'暂无违章哦'
    model.new_plate_number(plateNumber,engineNumber)
    #print content
    return content[:450] + (u'（未完整显示）' if len(content) > 450 else '')

def getrandcode():
    response = urllib2.urlopen('http://jjzd.nmgat.gov.cn/VerifyCodeServlet?timestamp=' + str(int(time.time())))
    imgdata = response.read()
    #f = file('./' + str(int(time.time())) + '.jpg', 'wb')
    #f.write(imgdata)
    #f.close()
    code = ocr.Pic_Reg(StringIO(imgdata))
    cookie = response.info().getheader('Set-Cookie').split(';')[0]
    print cookie
    print code
    return [code,cookie]
def _search(lastContent,content):
	VIN = content.strip().upper()
	ipAddress = model.get_a_ipaddress_available()
	print ipAddress
	if ipAddress:
		content = search(lastContent,VIN)
	else:
		content = u'由于资源限制，小道这里提供的查询次数是有限的，只能明天再试了'
	return content

def getcode():
    last_randcode = model.last_randcode()
    if last_randcode:
        now = datetime.datetime.now()
        if math.floor((( now - last_randcode['gettime']).seconds) / 60) < 10:
            return
    while True:
        code = getrandcode()
        if len(code[0]) == 4:
            model.new_randcode(code[0], code[1])
            return
def ipcheck():
    os.environ['disable_fetchurl'] = "1"
    proxy_list = model.get_ipaddress_unchecked()
    socket.setdefaulttimeout(2)
    for ipAddress in proxy_list:
        proxy_support = urllib2.ProxyHandler({'http':'http://' + ipAddress['address']})
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        try:
            f = opener.open('http://jjzd.nmgat.gov.cn/Query.jsp')
        except socket.timeout:
            model.ipaddress_remove(ipAddress['id'])
        except urllib2.HTTPError, err:
            model.ipaddress_remove(ipAddress['id'])
        except urllib2.URLError, err:
            model.ipaddress_remove(ipAddress['id'])
        except:
            model.ipaddress_remove(ipAddress['id'])
        model.ipaddress_checked(ipAddress['id'])
def getJiankong(wzdate):
    ##当获取的违章量>4000条时，也就是返回的字节数太大时，出错 httplib.IncompleteRead
    ##参考http://stackoverflow.com/questions/14149100/incompleteread-using-httplib
    httplib.HTTPConnection._http_vsn = 10
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
    ISOFORMAT='%Y-%m-%d' #设置输出格式
    print 'fetching jiankong at ' + wzdate.strftime(ISOFORMAT)
    req = urllib2.Request('http://jjzd.nmgat.gov.cn:9898/Announcement.jsp?GLBM=1501&&CurrDate=' + wzdate.strftime(ISOFORMAT))
    req.add_header('Referer', 'http://www.hhhtgajt.com/web/clwfgg.html')
    response = urllib2.urlopen(req, timeout=50)
    data = response.read()
    httplib.HTTPConnection._http_vsn = 11
    httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
    doc = html.document_fromstring(data)
    items = doc.xpath("//div[@class='Show7']")
    print len(items)
    regex = ur"\d+年\d+月\d+日".encode('utf8')
    p = re.compile(regex)
    if len(items) > 0:
        for item in items:
            text = item.attrib['onclick'].split('"')[5]
            lines = text.split('<br>')
            for line in lines:
                if line:
                    #print line.encode('utf8')
                    m = p.search(line.encode('utf8'))
                    if m.group(0):
                        wzdate = datetime.datetime.strptime(m.group(0), u"%Y年%m月%d日".encode('utf-8'))
                        model.new_jiankong(item.text_content().encode('utf-8'), \
                                           line[line.find(u':') + 1:].encode('utf-8'), \
                                           wzdate)
	return len(items)