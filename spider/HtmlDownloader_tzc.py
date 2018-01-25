#coding:utf-8
import sys
sys.path.append('..')
import random 
import config_tzc
from db.DataStore_tzc import sqlhelper

import requests
import chardet 

class Html_Downloader(object):
	@staticmethod

	def download(url):
		try:
			print('begin download url')
			r = requests.get(url=url,headers = config_tzc.get_header(),timeout=config_tzc.TIMEOUT)
			r.encoding = chardet.detect(r.content)['encoding']
			if (not r.ok) or len(r.content) < 500:
				raise ConnectionError
				

			else:
				return r.text

		except Exception as e:
			print(e)
			#重试换下代理IP试试
			count = 0 
			proxylist = sqlhelper.select(10)
			if not proxylist:
				return None

			while count < config_tzc.RETRY_TIME:
				try:
					proxy = random.choice(proxylist)
					
					ip = prox[0]
					port = prox[1]
					proxies = {'http':'http://%s:%s' %(ip,port),'https':'https://%s:%s' %(ip,port)}

					r = requests.get(url=url,headers=config_tzc.get_header(),timeout=config_tzc.TIMEOUT,proxies=proxies)
					r.encoding = chardet.detect(r.content)['enconding']
					if (not r.ok) or len(r.content) < 500:
						raise ConnectionError

					else:
						return r.text 

				except Exception:
					count += 1 
			return None


if __name__ == '__main__':
		url = 'http://www.66ip.cn/index.html'
		c = Html_Downloader.download(url)
		print(c)
