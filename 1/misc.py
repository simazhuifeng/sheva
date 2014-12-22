# coding=utf8
import math
import model
from lxml import etree
import httplib

def xml2obj(xml):
	# XML
	root = etree.fromstring( xml )
	child = list( root )
	recv = {}
	for i in child:
			recv[i.tag] = i.text
	return recv



def url_ping(url):
	try:
		a = httplib.HTTPConnection('google.com')
		a.connect()
		return 1
	except httplib.HTTPException as ex:
		return 0
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