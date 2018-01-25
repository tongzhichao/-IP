#coding='utf-8'
from multiprocessing import Queue,Process,Value

from config_tzc import TASK_QUEUE_SIZE
from spider.ProxyCrawl_tzc import startProxyCrawl
from validator.Validator_tzc import validator
from db.DataStore_tzc import store_data
from api.apiserver_tzc import start_api_server
if __name__ == '__main__':
	DB_PROXY_NUM = Value('i',0)

	q1 = Queue(maxsize=TASK_QUEUE_SIZE)
	p0 = Process(target=start_api_server)
	p1 = Process(target=startProxyCrawl,args=(q1,DB_PROXY_NUM))
	q2 = Queue()
	p2 = Process(target = validator,args=(q1,q2))
	p3 = Process(target = store_data,args=(q2,))
	p0.start()
	p1.start()
	print('p1的进程号',p1.pid)
	p2.start()
	print('p2的进程号',p2.pid)
	p3.start()

	p1.join()
	p2.join()
	p3.join()