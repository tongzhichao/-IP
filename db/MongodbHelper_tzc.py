#coding:utf-8
import pymongo
import sys
sys.path.append('..')
from config_tzc import DB_CONFIG,DEFAULT_SCORE

from db.ISqlHelper_tzc import ISqlHelper 

class MongoHelper(ISqlHelper):
	def __init__(self):
		self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'],connect=False)


	def init_db(self):
		self.db = self.client.proxy
		self.proxys = self.db.proxys


	def drop_db(self):
		self.client.drop_database(self.db)

	def insert(self,value=None):
		if value:
			proxy = dict(ip=value['ip'],port=value['port'],types=value['types'],protocol=value['protocol'],
						country=value['country'],area=value['area'],speed=value['speed'],score=DEFAULT_SCORE)
			self.proxys.insert(proxy)

	def delete(self,conditions=None):
		if conditions:
			self.proxys.remove(conditions)
			return ('deleteNum','ok')

		else:
			return ('deleteNum','None')

	def update(self,conditions=None,value=None):
		if conditions and value:
			self.proxys.update(conditions,{'$set':value})
			return  {'updateNum':'ok'}

		else:
			return {'updateNum':'fail'}

	def select(self,count=None,conditions=None):
		if count:
			count = int(count)

		else:
			count = 0 

		if conditions:
			conditions = dict(conditions)
			conditions_name = ['types','protocol']
			for condition_name in conditions_name:
				value = conditions.get(condition_name,None)
				if value:
					conditions[condition_name] = int(value)
		else:
			conditions = {}
		print('mongodb select',conditions)

		items = self.proxys.find(conditions,limit=count).sort([('speed',pymongo.ASCENDING),('score',pymongo.DESCENDING)])
		results = []

		for item in items:
			result = (item['ip'],item['port'],item['score'])
			results.append(result)

		return results 


if __name__ == '__main__':
	sqlhelper = MongoHelper()
	sqlhelper.init_db()
	proxy={'ip':'192.168.1.3','port':80,'types':0,'protocol':0,'country':'中国','area':'广州','speed':11.23}

	sqlhelper.insert(proxy)
	#sqlhelper.update({'ip':'192.168.1.2','port':80},{'ip':'192.168.11.11','port':7878})
	print(sqlhelper.select(1))
	#print(sqlhelper.select(2,{'ip':'192.168.11.11','port':7878,'types':'0'}))
	#print(sqlhelper.delete({'ip':'192.168.1.1','port':80}))