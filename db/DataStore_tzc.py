import sys 
sys.path.append('..')
from config_tzc import DB_CONFIG
from util.exception_tzc import Con_DB_Fail

try:
	if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
		from db.MongodbHelper_tzc import MongoHelper as SqlHelper

	elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
		from db.RedisHelper_tzc import RedisHelper as SqlHelper
	else:
		from db.SqlHelper_tzc import SqlHelper as SqlHelper



	sqlhelper = SqlHelper()
	sqlhelper.init_db()

except Exception as e:
	raise Con_DB_Fail


def store_data(queue2):
	successNum = 0 
	failNum = 0 

	while True:
		try:
			print('queue2的长度',queue2.qsize())
			proxy = queue2.get(timeout=300)

			if proxy:
				print('准备插入数据的代理IP为：',proxy)
				sqlhelper.insert(proxy)
				successNum += 1 
			else:
				failNum += 1

			print('IPProyPool----->>>>>Success ip num:%d,Fail ip num:%d' % (successNum,failNum))

		except Exception as e:
			
			print(e)
			print('插入数据库出错')
