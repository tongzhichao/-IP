import sys,datetime
sys.path.append('..')
from config_tzc import DB_CONFIG,DEFAULT_SCORE
from sqlalchemy import create_engine,Column,Integer,VARCHAR,String,DateTime,Numeric

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db.ISqlHelper_tzc import ISqlHelper
BaseModel = declarative_base()

class Proxy(BaseModel):
	__tablename__ = 'proxys_tzc'
	id = Column(Integer,primary_key = True,autoincrement=True)
	ip = Column(VARCHAR(16),nullable=False)
	port = Column(Integer,nullable=False)
	types = Column(Integer,nullable=False)
	protocol = Column(Integer,nullable=False,default=0)
	country = Column(VARCHAR(100),nullable=False)
	area = Column(VARCHAR(100),nullable = False)
	updatetime = Column(DateTime(),default=datetime.datetime.utcnow)
	speed = Column(Numeric(5,2),nullable=False)
	score = Column(Integer,nullable=False,default=DEFAULT_SCORE)
class SqlHelper(ISqlHelper):
	params = {'ip':Proxy.ip,'port':Proxy.port,'types':Proxy.types,'protocol':Proxy.protocol,
				'country':Proxy.country,'area':Proxy.area,'score':Proxy.score}

	def __init__(self):
		if 'sqlite' in DB_CONFIG['DB_CONNECT_STRING']:
			connect_args = {'check_same_thread':False}
			self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'],echo=False,connect_args=connect_args)


		else:
			print('mysql数据库')
			self.engine = create_engine(DB_CONFIG['DB_CONNECT_STRING'],echo=False)
		DB_Session = sessionmaker(bind = self.engine)
		self.session = DB_Session()

	def init_db(self):
		BaseModel.metadata.create_all(self.engine)

	def drop_db(self):
		BaseModel.metadata.drop_all(self.engine)
	def insert(self,value):
		proxy = Proxy(ip=value['ip'],port=value['port'],types=value['types'],protocol=value['protocol'],
					country=value['country'],area = value['area'],speed=value['speed'])
		self.session.add(proxy)
		self.session.commit()
	def select(self,count=None,conditions=None):
		if conditions:
			conditon_list = []
			for key in list(conditions.keys()):
				if self.params.get(key,None):
					conditon_list.append(self.params.get(key)==conditions.get(key))
			conditions = conditon_list

		else:
			conditions = []
		query = self.session.query(Proxy.ip,Proxy.port,Proxy.score)
		#print(query)
		#print('------')
		if len(conditions) > 0 and count:

			for condition in conditions:
				query = query.filter(condition)
				#print(condition)
				#print(query)
			return query.order_by(Proxy.score.desc(),Proxy.speed).limit(count).all()

		elif count:
			return query.order_by(Proxy.score.desc(),Proxy.speed).limit(count).all()

		elif len(conditions) > 0:
			for condition in conditions:
				query = query.filter(condition)

			return query.order_by(Proxy.score.desc(),Proxy.speed).all()
		else:

			return query.order_by(Proxy.score.desc(),Proxy.speed).all()



	def delete(self,conditions=None):
		if conditions:
			condition_list = []
			for key in list(conditions.keys()):
				if self.params.get(key):
					condition_list.append(self.params.get(key)==conditions.get(key))

			conditions = condition_list
			query = self.session.query(Proxy)
			for condition in conditions:
				query = query.filter(condition)
			deleteNum = query.delete()
			self.session.commit()
		else:
			deleteNum = 0 
		return ('deleteNum',deleteNum)

	def update(self,conditions=None,value=None):
		if conditions and value:
			condition_list = []
			for key in list(conditions.keys()):
				if self.params.get(key,None):
					condition_list.append(self.params.get(key)==conditions.get(key))
			conditions = condition_list
			query = self.session.query(Proxy)
			for condition in conditions:
				query = query.filter(condition)
			#print(query)
			updatevalue = {}	
			for key in list(value.keys()):
				if self.params.get(key,None):
					updatevalue[self.params.get(key,None)] = value.get(key)

				updateNum = query.update(updatevalue)
				self.session.commit()

		else:
			updateNum = 0 

		return {'updateNum':updateNum}		



if __name__ == '__main__':
	sqlhelper = SqlHelper()
	sqlhelper.init_db()
	#count=5
	#ipxoy = {'ip': '192.168.1.1', 'port': 8080}
	#value = {'types':2}
#	s = sqlhelper.select(conditions=ipxoy)
#	print(s)
	## q= sqlhelper.update(ipxoy,value)
	#print(q)
	#print(sqlhelper.select())
	#print(sqlhelper.delete(ipxoy))
	proxy={'ip':'123.173.1.1','port':80,'types':0,'protocol':0,'country':'中国','area':'广州','speed':11.23}
	sqlhelper.insert(proxy)