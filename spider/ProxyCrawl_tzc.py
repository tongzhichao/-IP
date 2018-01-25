#coding=utf-8
import sys
sys.path.append('..')
import gevent,time
from db.DataStore_tzc import sqlhelper
from multiprocessing import Value,Queue,Process
from validator.Validator_tzc import detect_from_db
from config_tzc import MAX_CHECK_CONCURRENT_PER_PROCESS,MINNUM,parserList,MAX_DOWNLOAD_CONCURRENT,UPDATE_TIME

from spider.HtmlDownloader_tzc import Html_Downloader
from spider.HtmlParser_tzc import Html_Parser
def startProxyCrawl(queue,db_proxy_num):
	crawl = ProxyCrawl(queue,db_proxy_num)
	crawl.run()



class ProxyCrawl(object):
	proxies = set()

	def __init__(self,queue,db_proxy_num):
		#self.crawl_pool = Pool(THREADNUM)
		self.queue = queue
		self.db_proxy_num = db_proxy_num
	

	def run(self):
		while  True:
			self.proxies.clear()
			str = 'IPProxyPool---->>>beginging'
			print(str)

			proxylist = sqlhelper.select()
			print('数据库所有的代理IP数：',proxylist)
			
			spawns = []

			for proxy in proxylist:
				
				spawns.append(gevent.spawn(detect_from_db,proxy,self.proxies))
#				print(len(spawns))
				if len(spawns) >= MAX_CHECK_CONCURRENT_PER_PROCESS:
					print('开始启动协程组',len(spawns))
					gevent.joinall(spawns)
					spawns = []
			gevent.joinall(spawns)#该句是为了防止协程组数量不大于MAX_CHECK_CONCURRENT_PER_PROCESS，
			#而导致计算db_proxy_num为空
			self.db_proxy_num.value = len(self.proxies)
			print('检验后剩余的IP',self.db_proxy_num.value)
			print('IPProxyPool---->>>>db exists ip:%d' % len(self.proxies))

			if len(self.proxies) < MINNUM:
				print('代理IP数量小于MINNUM，准备开启爬取')
				spawns = []
				for p in parserList:
					spawns.append(gevent.spawn(self.crawl,p))
					if len(spawns) >= MAX_DOWNLOAD_CONCURRENT:
						gevent.joinall(spawns)
						spawns = []

			else:
				print('当前可用IP已足够，等待UPDATTIME时间后才检验是否需要爬取')

			time.sleep(UPDATE_TIME)

	def crawl(self,parser):
		html_parser = Html_Parser()
		for url in parser['urls']:
			print('开始爬取的URL为：',url)
			response = Html_Downloader.download(url)
			if response is not None:
				proxylist = html_parser.parse(response,parser)
				for proxy in proxylist:
					proxy_str = '%s:%s' %(proxy['ip'],proxy['port'])
					if proxy_str not in self.proxies:
						while True:
#							print('队列的长度',self.queue.qsize())
							if self.queue.full():
								time.sleep(0.1)
							else:
								self.queue.put(proxy)
								break


if __name__ == '__main__':
	q1 = Queue()
	DB_PROXY_NUM = Value('i',0)
	
	startProxyCrawl(q1,DB_PROXY_NUM)
	

