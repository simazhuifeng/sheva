# coding=utf8
import model
import re
import bike
import weizhang
from context import Context 

def route(recv):
	currentContext = Context(recv['FromUserName'])
	lastContent = currentContext.lastConversation()
	lastContent = lastContent.get('Content') if lastContent else None
	lastContent = lastContent.strip().upper() if lastContent else None
	#contentTpl = u'>>%s\n--------------------\n%s\n由【%s】于 %s 提供'
	contentTpl = u'>>%s\n--------------------\n%s'
	busRe = re.compile(u'^(\d+路|\S+线)$')
	#roadRe = re.compile(u'\D+[街路环桥巷道]$')
	
	content = ''
	if recv.get('Event') and recv['Event'] == 'subscribe':
		content = u'''小伙伴，你来啦~\n\n道哥这里有一些交通出行和招聘方面的消息，当然也侃一些别的，各取所需咯。\n\n小道机器人可以帮你做一些事儿哦：\n\n查违章\n查公共自行车位置\n查公交\n查附近的PM2.5观测值'''
		return content
	if recv['MsgType'] == 'location':
		print 'request bike & air'
		return bike.buildBike(recv)
	if recv.get('Content') and any(recv['Content'] in nickname['name'] for nickname in model.get_nickname_all()) :
		items = model.get_item_by_text(recv['Content'])
		for item in items:
			itemid = item['itemid']
			event = model.get_event(itemid)
			if event:
				#content += contentTpl % (item['name'],event['content'],event['commit'],event['time'].strftime('%m/%d %H:%M'))
				if("$$" in event['content']): #is a article
					content += event['content']
				else:
					content += contentTpl % (item['name'],event['content'])
		return content
	if recv.get('Content') and busRe.match(recv['Content']):
		content = u'<a href="http://m.8684.cn/huhehaote_bus">点击进入查询界面</a>'
		return content
	plateNumberRe = re.compile(ur'[\u8499|\u4EAC|\u9655|\u664B]\w{6}')
	OUTFORMAT = u'%Y-%m-%d'
	if recv.get('Content') and plateNumberRe.match(recv['Content'].strip().replace(" ", "").upper()):
		jiankongs = model.get_jiankong(recv.get('Content').upper())
		if len(jiankongs) == 0:
			content = u'暂时没有被监控设备抓拍的记录哦'
		else:
			content += u'发现至少一条记录,'
			content += u'最新一条记录时间为 ' 
			content += jiankongs[0]['wzdate'].strftime(OUTFORMAT).encode('utf-8')
			content += ' <a href=\'http://1.hushixiaodao.sinaapp.com/jiankong?chepai='
			content += recv.get('Content').upper() 
			content += u'\'>查看抓拍记录</a>'
		print content
		return content
#	content = u'''机器人小道不知道怎么回答你...
#--------------------
#小道已打听到的信息有修路期间的道路信息以及公交车绕行信息,发“石羊桥路”或者“76路”试试？
#>>有什么想打听的可以给小道留言，小道去试试'''  
	return content