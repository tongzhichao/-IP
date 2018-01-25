#
import sys
sys.path.append('..')
import config_tzc

class Con_DB_Fail(Exception):
	def __str__(self):
		str = '使用DB_CONNECT_STRING:%s---连接数据库失败' % config_tzc.DB_CONFIG['DB_CONNECT_STRING']

		return str 