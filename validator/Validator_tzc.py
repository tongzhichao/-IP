#coding:utf-8
import sys,os
sys.path.append('..')
import config_tzc
import time,chardet
import requests,psutil
from db.DataStore_tzc import sqlhelper
from multiprocessing import Queue,Process
import gevent
def detect_from_db(proxy,proxies):
	proxy_dict = {'ip':proxy[0],'port':proxy[1]}

	result = detect_proxy(proxy_dict)
	if result:
		proxy_str = '%s:%s' %(proxy[0],proxy[1])
		proxies.add(proxy_str)

	else:
		if proxy[2] < 1:
			print('该代理IP即将被删除',proxy[0])
			sqlhelper.delete(proxy_dict)

		else:
			score = proxy[2] - 1 
			print('该代理IP分数减1',proxy[0])
			sqlhelper.update(proxy_dict,{'score':score})
			proxy_str = '%s:%s' %(proxy[0],proxy[1])
			proxies.add(proxy_str)


def validator(queue1,queue2):

	tasklist = []
	pro_pool = {}
	cntl_q = Queue()
	while True:
#		print('cntl_q的长度',cntl_q.qsize())
		if not cntl_q.empty():
			try:
				pid = cntl_q.get()
				pro_pool.pop(pid)
				pro_ps = psutil.Process(pid)
				pro_ps.wait()
				print('kill process',pid)
			except Exception as e:
				print('can not to kill pid')
				pass

		try:
#			longqueue = cntl_q.qsize()
#			print(longqueue)
			longqueue = len(pro_pool)
			if longqueue >= config_tzc.MAX_CHECK_PROCESS:
				time.sleep(config_tzc.CHECK_WAIT_TIME)
				print('进程数太多，暂时停留',longqueue)
				continue
#				break


			proxy = queue1.get()
			tasklist.append(proxy)
#			print('tasklit长度',len(tasklist))
			if len(tasklist) >= config_tzc.MAX_CHECK_CONCURRENT_PER_PROCESS:
				p = Process(target=process_start,args=(tasklist,queue2,cntl_q))
				p.start()
				print('产生的新进程',p.pid)
				pro_pool[p.pid] = p 
#				cntl_q.put(p.pid)
				tasklist =[]
				

		except Exception as e:
			print(e)
			if len(tasklist) > 0:
				p = Process(target=process_start,args=(tasklist,queue2,cntl_q))
				p.start()
				print('产生的新进程',p.pid)
				pro_pool[p.pid] = p 
#				cntl_q.put(p.pid)
				tasklist =[]
			



def process_start(tasklist,queue2,cntl_q):
	
	spawns = []
	for task in tasklist:
		spawns.append(gevent.spawn(detect_proxy,task,queue2))
		
	gevent.joinall(spawns)
	pid = os.getpid()
	cntl_q.put(pid)
	print('校验完成',pid)
	








#protocol为协议类型，0：http,1:https,2:http/https
#type为类型，	0: 高匿,1:匿名,2 透明
#speed为速度，使用代理IP访问的速度
def detect_proxy(proxy,queue2=None):
	ip = proxy['ip']
	port = proxy['port']
	proxies = {'http':'http://%s:%s'%(ip,port),'https':'https://%s:%s'%(ip,port)}

	protocol,types,speed = getattr(sys.modules[__name__],config_tzc.CHECK_PROXY['function'])(proxies)
	if protocol >= 0:
		proxy['protocol'] = protocol
		proxy['types'] = types
		proxy['speed'] = speed 
	else:
		proxy = None 
		print('该代理IP不可用',ip)
	if queue2:
		queue2.put(proxy)
	return proxy 


def baidu_check(proxies):
	protocol = -1 
	types = -1 
	speed = -1 

	try:
		start = time.time()
#		r = requests.get(url = 'https://www.baidu.com',headers=config_tzc.get_header(),timeout=config_tzc.TIMEOUT,proxies=proxies)
#		r.encoding = chardet.detect(r.content)['encoding']
		r = requests.head(url = 'https://www.baidu.com',headers=config_tzc.get_header(),timeout=config_tzc.TIMEOUT,proxies=proxies)
		if r.ok:
			print('代理IP访问百度成功')
			speed = round(time.time() - start,2)
			protocol = 0 
			types = 0 

		else:
			speed = -1 
			protocol = -1 
			types = -1 
	except Exception as e:
		speed = -1 
		protocol = -1 
		types = -1 

	return protocol,types,speed 