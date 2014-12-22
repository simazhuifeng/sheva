# coding=utf8
import model
import misc

class Context:
	openid = ''
	def __init__(self,openid):
		self.openid = openid

	def lastConversation(self):
		c = model.last_conversation(self.openid)
		if c:
			return misc.xml2obj(c['content'])
		return None