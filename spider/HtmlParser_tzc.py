#coding:utf-8
import sys
sys.path.append('..')
import base64 
from config_tzc import QQWRY_PATH,DEFAULT_SCORE,CHINA_AREA
import requests

import re 
from lxml import etree 
from util.compatibility_tzc import text_
from util.IPAddress_tzc import IPAddresss
class Html_Parser(object):
	def __init__(self):
		self.ips = IPAddresss(QQWRY_PATH)
		
	def parse(self,response,parser):
		
		if parser['type'] == 'xpath':
			return self.XpathParser(response,parser)

		elif parser['type'] == 'regular':
			return self.RegularParser(response,parser)

		elif parser['type'] == 'module':
			return getattr(self,parser['moduleName'],None)(response,parser)

		else:
			return None 

	def AuthCountry(self,addr):
		for area in CHINA_AREA:
			
			if text_(area) in addr:
				return True
				print('jinrugaihanshu')

			return False 

	def XpathParser(self,response,parser):
		print('begin xpathparser')
		proxylist = []
		root = etree.HTML(response)
		proxys = root.xpath(parser['pattern'])
		print(proxys)
		for proxy in proxys:
			try:
				ip = proxy.xpath(parser['position']['ip'])[0].text

				port = proxy.xpath(parser['position']['port'])[0].text
				print(ip)
				types = 0 
				protocol = 0 
				addr = self.ips.getIpAddr(self.ips.str2ip(ip))
				print(addr)
				country = text_('')
				area = text_('')
				print('--------------',area)
#				print(self.AuthCountry(addr))
				
				if text_('省') in addr or self.AuthCountry(addr):
					print('nei')
					country = text_('国内')	
					area = addr 
				else:
					print('wai')
					country = text_('国外')
					area = addr 
##				print(ip,port,area,country)
			except Exception as e:
				print(e)
				continue 
			proxy = {'ip':ip,'port':int(port),'types':int(types),
			'protocol':int(protocol),'country':country,
			'area':area,'speed':DEFAULT_SCORE }
			
			proxylist.append(proxy)

		return proxylist


if __name__=='__main__':
	url = 'http://www.66ip.cn/areaindex_1/1.html'
	r = requests.get(url)
	s = r.content
	
	parser = {
		'urls':['http://www.66ip.cn/index.html'],
		'type':'xpath',
		'pattern': ".//*[@id='footer']/div/table/tr[position()>1]",
		'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[4]', 'protocol': ''}
	}
	c = Html_Parser()


	proxy = c.parse(s,parser)
	print(proxy)