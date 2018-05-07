from flask import Blueprint, request, session, jsonify, url_for
from redissession import RedisSessionInterface
from .iotku_database import Iotku
from .natslib import NATS
import os, hashlib

name = 'api'
api = Blueprint(name, __name__)
iotku = Iotku()
c = NATS()

#---------------------API---------------------------

#---------------------CORE---------------------------
@api.route('/api/register', methods=['POST'])
def register():
	content = request.get_json(silent=True)
	if all(x in content.keys() for x in ["email","password"]):
		email = content["email"]
		password = content["password"]
		if not iotku.find_user(email=email):
			iotku.add_user(email=email,password=password)
			session['logged_in'] = True
			session['email'] = email
			session['api_key'] = hashlib.md5(email.encode('utf-8')).hexdigest()
			return jsonify({'result': True})
		else:
			return jsonify({'result': False,'reason':'An account with the same email exists'})
	else: 
		return jsonify({'result': False,'reason':'Invalid format'})

@api.route('/api/connect', methods=['POST'])
def connect():
	content = request.get_json(silent=True)
	if content and all(x in content.keys() for x in ["api_key","device_id"]):
		try:
			api_key = content['api_key']
			device_id = content['device_id']
			user = iotku.find_user(api_key=api_key)
			if user:
				if user.find_device(device_id): 
					session['logged_in'] = True
					session['api_key'] = content['api_key']
					session['device_id'] = content['device_id']
					return jsonify({'result': True})
				else:
					return jsonify({'result': False,'reason': 'Invalid Device ID'})
			else:
				return jsonify({'result': False,'reason': 'Invalid API key'})
		except Exception as e:
			print('Unknown error at do_login: ' + str(e))
			return jsonify({'result': False, 'reason': 'Unknown Error'})
	elif content and all(x in content.keys() for x in ["email","password"]):
		email = content['email']
		password = content['password']
		user = iotku.find_user(email=email, password=password)
		if user:
			session['logged_in'] = True
			session['api_key'] = user.get_api_key()
			session['email'] = content['email']
			return jsonify({'result': True})
		else:
			return jsonify({'result': False,'reason':'Wrong email or password'})
	else:
		return jsonify({'result': False,'reason': "Invalid format"})

@api.route('/api/disconnect')
def disconnect():
	#Membuang session. {dev aviezab 2018.03.08}
	session.pop('email', None)
	session.pop('api_key', None)
	session.pop('device_id', None)
	session['logged_in'] = False
	return jsonify({'result': True})

@api.route('/api/is_logged_in')
def is_logged_in():
	if session.get('logged_in'):
		return jsonify({'result': True})
	else:
		return jsonify({'result': False})
#---------------------/CORE---------------------------

#------------------USER-------------------------
@api.route('/api/user_email', methods=['GET'])
def user_email():
	if all(x in session.keys() for x in ["logged_in","email"]):
		return jsonify({'result': session['email']})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/user_api_key', methods=['GET'])
def user_api_key():
	if all(x in session.keys() for x in ["logged_in","api_key"]):
		return jsonify({'result': session['api_key']})
	else:
		return jsonify({'result':False,'reason':'Not connected to any account.'})

@api.route('/api/user_time_added', methods=['GET'])
def user_time_added():
	if all(x in session.keys() for x in ["logged_in","email"]):
		user = iotku.find_user(email=session["email"])
		return jsonify({'result':user.get_time_added()})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/user_total_device', methods=['GET'])
def user_total_device():
	if all(x in session.keys() for x in ["logged_in","email"]):
		user = iotku.find_user(email=session["email"])
		return jsonify({'result': user.get_total_device()})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/add_device', methods=['POST'])
def add_device():
	if all(x in session.keys() for x in ["logged_in","email"]):
		content = request.get_json(silent=True)
		if all(x in content.keys() for x in ["device_id","device_name"]):
			device_id = content['device_id']
			device_name = content['device_name']
			if device_id and device_name:
				user = iotku.find_user(email=session["email"])
				if not user.find_device(device_id):
					user.add_device(device_id,device_name)
					return jsonify({'result': True})
				else:
					return jsonify({'result': False, 'reason': "Device ID exists"})
			else:
				return jsonify({'result': False, 'reason': "Device ID and/or device name cannot be empty"})
		else:
			return jsonify({'result': False, 'reason': 'Invalid format'})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})

@api.route('/api/remove_device', methods=['POST'])
def remove_device():
	if all(x in session.keys() for x in ["logged_in","email"]):
		content = request.get_json(silent=True)
		if all(x in content.keys() for x in ["device_id"]):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			if user.find_device(device_id):
				user.remove_device(device_id)
				return jsonify({'result': True})
			else:
				return jsonify({'result': False, 'reason': "Device ID not found"})
		else:
			return jsonify({'result': False, 'reason': 'Invalid format'})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})

@api.route('/api/device_list', methods=['GET'])
def device_list():
	if all(x in session.keys() for x in ["logged_in","email"]):
		user = iotku.find_user(email=session["email"])
		devices = user.get_device_list()
		device_list = [{'device_id':x.get_device_id(),'device_name':x.get_device_name()} for x in devices]
		return jsonify({'result':device_list})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/USER-------------------------

#------------------DEVICE-------------------------

@api.route('/api/device_name', methods=['GET'])
def device_name():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if content.get('device_id'):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				return jsonify({'result':device.get_device_name()})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/device_time_added', methods=['GET'])
def device_time_added():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if content.get('device_id'):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				return jsonify({'result':device.get_time_added()})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/device_total_sensor', methods=['GET'])
def device_total_sensor():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if content.get('device_id'):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				return jsonify({'result':device.get_total_sensor()})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/add_sensor', methods=['POST'])
def add_sensor():
	if all(x in session.keys() for x in ["logged_in","email"]):
		content = request.get_json(silent=True)
		if all(x in content.keys() for x in ["device_id","sensor_id","sensor_name"]):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor_id, sensor_name = content["sensor_id"],content["sensor_name"]
				if not device.find_sensor(sensor_id):
					device.add_sensor(sensor_id,sensor_name)
					return jsonify({'result': True})
				else:
					return jsonify({'result': False, 'reason': "Sensor ID exists"})
			else:
				return jsonify({'result': False, 'reason': "Device ID not found"})
		else:
			return jsonify({'result': False, 'reason': 'Invalid format'})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})

@api.route('/api/remove_sensor', methods=['POST'])
def remove_sensor():
	if all(x in session.keys() for x in ["logged_in","email"]):
		content = request.get_json(silent=True)
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor_id = content["sensor_id"]
				if device.find_sensor(sensor_id):
					device.remove_sensor(sensor_id)
					return jsonify({'result': True})
				else:
					return jsonify({'result': False, 'reason': "Sensor not found"})
			else:
				return jsonify({'result': False, 'reason': "Device ID not found"})
		else:
			return jsonify({'result': False, 'reason': 'Invalid format'})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})

@api.route('/api/device_sensor_list', methods=['GET'])
def device_sensor_list():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if content.get('device_id'):
			device_id = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensors = device.get_sensor_list()
				sensor_id = [x.get_sensor_id() for x in sensors]
				sensor_name = [x.get_sensor_name() for x in sensors]
				time_added = [x.get_time_added() for x in sensors]
				sensor_list = [{'sensor_id':x,'sensor_name':y,'time_added':z} for x,y,z in zip(sensor_id, sensor_name, time_added)]
				return jsonify({'result':sensor_list})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/DEVICE-------------------------

#------------------SENSOR-------------------------
@api.route('/api/sensor_name', methods=['GET'])
def sensor_name():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			device_id = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					return jsonify({'result':sensor.get_sensor_name()})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/sensor_time_added', methods=['GET'])
def sensor_time_added():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			device_id = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
						return jsonify({'result':sensor.get_time_added()})
				else:
						return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False,'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/sensor_data', methods=['GET'])
def sensor_data():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			try:
				from_number = int(content['from'])
				assert from_number >= 0
			except:
				from_number = 0
			try:
				to_number = int(content['to'])
				assert from_number < to_number and to_number < 25
			except:
				to_number = from_number + 25
			device_id = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session['email'])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					data_collection = sensor.get_data(from_number,from_number+25)
					return jsonify({'result':data_collection})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/sensor_total_data_entry', methods=['GET'])
def sensor_total_data_entry():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			device_id = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					total_entry = sensor.get_total_data_entry()
					return jsonify({'result':total_entry})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/sensor_last_data_added_time', methods=['GET'])
def sensor_last_data_added_time():
	content = request.args
	if all(x in session.keys() for x in ["logged_in","email"]):
		if all(x in content.keys() for x in ["device_id","sensor_id"]):
			device_id = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					last_time = sensor.get_last_data_added_time()
					return jsonify({'result':last_time})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'Device ID not found'})
		else:
			return jsonify({'result':False,'reason':"Invalid format"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@api.route('/api/post', methods=['POST'])
def post_sensor_data():
	if all(x in session.keys() for x in ["logged_in","api_key","device_id"]):
		content = request.get_json(silent=True)
		if all(x in content.keys() for x in ["data","sensor_id"]):
			data = content['data']
			device_id = session['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(api_key=session['api_key'])
			device = user.find_device(device_id)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					formatted = session['api_key'].encode("ascii").hex() + ' , ' + device_id.encode("ascii").hex() + ' , ' + sensor_id.encode("ascii").hex() + ' , ' + data.encode("ascii").hex()
					c.publish(subject='post', payload=bytes(formatted, 'utf-8'))
					return jsonify({'result': True})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'Device ID not found'})
		else:
			return jsonify({'result': False,'reason': "Invalid format"})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account / Invalid login type'})
#------------------/SENSOR-------------------------

#---------------------MISC---------------------------
@api.route('/api/url', methods=['GET'])
def url_list():
	api_functions = [
						# CORE
						'register',
						'connect',
						'disconnect',
						'is_logged_in',

						# USER
						'user_email',
						'user_api_key',
						'user_time_added',
						'user_total_device',
						'add_device',
						'remove_device',
						'device_list',

						# DEVICE
						'device_name',
						'device_time_added',
						'device_total_sensor',
						'add_sensor',
						'remove_sensor',
						'device_sensor_list',

						# SENSOR
						'sensor_name',
						'sensor_time_added',
						'sensor_data',
						'sensor_total_data_entry',
						'sensor_last_data_added_time',
						'post_sensor_data',

						# MISC
						'url_list'
					]
	api_functions_url = {x: url_for(name + '.' + x) for x in api_functions}
	return jsonify({'result':api_functions_url})
#---------------------/MISC---------------------------

#--------------------/API---------------------------