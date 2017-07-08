from flask import Flask,request, render_template, redirect, flash, url_for, g, session, jsonify, make_response
from celery import Celery
from flask_restful import Resource, Api
from webargs import fields, validate
import time
import datetime
from webargs.flaskparser import use_args, use_kwargs, parser, abort
from celery.task.control import inspect,revoke
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
api = Api(app)

created_tasks = []
killed_tasks = []

@celery.task
def my_background_task(arg1):
	endTime = datetime.datetime.now() + datetime.timedelta(seconds=arg1)
	while True:
		if datetime.datetime.now() > endTime:
			break 
	return {'status':"ok"}

class Status(Resource):
	add_args = {
		'connid': fields.Int(required=True)
		}


	@use_kwargs(add_args)
	def get(self,connid):
		i = celery.control.inspect()
		m = i.active()
		data = m['celery@worker1']
		id_list = []
		for i in range(0,len(data)):
			id_list.append(int(data[i]['id']))
		if connid in id_list:
			return {"status":"running"}
		elif connid in killed_tasks:
			return {"status":"killed"}
		elif connid not in created_tasks:
			return {"status": "Invalid Connid"}
		else:
			return {"status":"ok"}



class Request(Resource):
	add_args = {
		'connid': fields.Int(required=True),
		'timeout': fields.Int(required=True)
		}


	@use_kwargs(add_args)
	def get(self,connid,timeout):
		my_background_task.apply_async(args=[timeout],task_id=str(connid))
		created_tasks.append(int(connid))
		return {"address":"/api/status?connid="+str(connid)}

class ServerStatus(Resource):
	def get(self):
		i = celery.control.inspect()
		m = i.active()
		data = m['celery@worker1']
		json_data = {}
		if len(data) == 0:
			return {"status":"No tasks running"}
		else:
			for i in range(0,len(data)):
				left_time  = int((data[i]['args'].replace("[",'')).replace("]",'')) - int(time.time() - data[i]['time_start'])
				json_data.update({data[i]['id']:left_time})
			return json_data

class Apikill(Resource):
	def put(self):
		content = request.json
		i = celery.control.inspect()
		m = i.active()
		data = m['celery@worker1']
		id_list = []
		for i in range(0,len(data)):
			id_list.append(data[i]['id'])
		if content['connid'] in id_list:
			killed_tasks.append(int(content['connid']))
			celery.control.revoke(str(content['connid']),terminate=True)
			return {"status": "ok"}
		else:
			return {"status": "Invalid connection Id" + content['connid']}

api.add_resource(Request, '/api/request')
api.add_resource(ServerStatus, '/api/serverStatus')
api.add_resource(Apikill, '/api/kill')
api.add_resource(Status, '/api/status')


if __name__ == '__main__':
	#http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
	#http_server.serve_forever()
	app.run(debug=True)