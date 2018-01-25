#coding:utf-8
import sys
sys.path.append('..')

from db.DataStore_tzc import sqlhelper
from db.SqlHelper_tzc import Proxy

import config_tzc
import web,json

urls = (
	'/','select',
	'/delete','delete'
	)


def start_api_server():
	sys.argv.append('0.0.0.0:%s' % config_tzc.API_PORT)
	app = web.application(urls,globals())
	app.run()


class select(object):
	def GET(self):
		inputs = web.input()
		print(inputs)
		json_result = json.dumps(sqlhelper.select(inputs.get('count',None),inputs))
		return json_result


class delete(object):
	params = {}
	def GET(self):
		inputs = web.input()
		print(inputs)
		json_result = json.dumps(sqlhelper.delete(inputs))
		return json_result

if __name__=='__main__':
	sys.argv.append('0.0.0.0:8000')
	app = web.application(urls,globals())
	app.run()