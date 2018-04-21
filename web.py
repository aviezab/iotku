from flask import *
from redissession import RedisSessionInterface
from iotku_database import Iotku
import os, hashlib

app = Flask(__name__, static_url_path='/static')
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()
iotku = Iotku()

@app.route("/", methods=['GET'])
def index():
	if session.get('logged_in') and session.get('email'):
		return render_template('dashboard.html')
	else:
		return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
	if request.form['password'] and request.form['email']:
		if not iotku.find_user(email=request.form['email']):
			iotku.add_user(email=request.form['email'],password=request.form['password'])
			session['logged_in'] = True
			session['email'] = request.form['email']
			session['api_key'] = hashlib.md5(request.form['email'].encode('utf-8')).hexdigest()
			return jsonify({'result': True})
		return jsonify({'result': False,'reason':'An account with the same email exists'})
	return jsonify({'result': False,'reason':'Invalid format'})

@app.route('/device_list', methods=['GET'])
def device_list():
	if session.get('logged_in') and session.get('email'):
		return render_template('device.html')
	else:
		return redirect(url_for('index'))

@app.route('/<device_id>', methods=['GET'])
def device(device_id):
	if session.get('logged_in') and session.get('email'):
		return render_template('device.html')
	else:
		return redirect(url_for('index'))

@app.route('/sensor', methods=['GET'])

#---------------------API---------------------------

#---------------------CORE---------------------------
@app.route('/api/connect', methods=['POST'])
def connect():
	if request.is_json:
		content = request.get_json(silent=True)
		if content:
			if 'api_key' in content.keys() and 'device_id' in content.keys():
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
			elif 'email' in content.keys() and 'password' in content.keys():
				email = content['email']
				password = content['password']
				user = iotku.find_user(email=email, password=password)
				if user:
					session['logged_in'] = True
					session['api_key'] = user.api_key
					session['email'] = content['email']
					return jsonify({'result': True})
				else:
					return jsonify({'result': False,'reason':'Wrong email or password'})
	return jsonify({'result': False,'reason': "Invalid format"})

@app.route('/api/disconnect')
def disconnect():
	#Membuang session. {dev aviezab 2018.03.08}
	session.pop('email', None)
	session.pop('api_key', None)
	session.pop('device_id', None)
	session['logged_in'] = False
	if request.method == 'GET':
		return redirect(url_for('index'))
	else:
		return jsonify({'result': True})

@app.route('/api/is_logged_in')
def is_logged_in():
	if session.get('logged_in'):
		return jsonify({'result': True})
	else:
		return jsonify({'result': False})
#---------------------/CORE---------------------------

#------------------USER-------------------------
@app.route('/api/get_user_email', methods=['GET'])
def get_user_email():
	if session.get('logged_in') and session.get('email'):
		return jsonify({'result': session['email']})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_user_api_key', methods=['GET'])
def get_user_api_key():
	if session.get('logged_in') and session.get('api_key'):
		return jsonify({'result': session['api_key']})
	else:
		return jsonify({'result':False,'reason':'Not connected to any account.'})

@app.route('/api/get_user_time_added', methods=['GET'])
def get_user_time_added():
	if session.get('logged_in') and session.get('email'):
		user = iotku.find_user(email=session["email"])
		return jsonify({'result':user.get_time_added()})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_user_total_device', methods=['GET'])
def get_user_total_device():
	if session.get('logged_in') and session.get('email'):
		user = iotku.find_user(email=session["email"])
		return jsonify({'result': user.get_total_device()})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_device_list', methods=['GET'])
def get_device_list():
	if session.get('logged_in') and session.get('email'):
		user = iotku.find_user(email=session["email"])
		devices = user.get_device_list()
		device_list = [{'device_id':x.get_device_id(),'device_name':x.get_device_name()} for x in devices]
		return jsonify({'result':device_list})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/USER-------------------------

#------------------DEVICE-------------------------

@app.route('/api/get_device_name', methods=['GET'])
def get_device_name():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id'):
			ip_address = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				return jsonify({'result':device.get_device_name()})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_device_time_added', methods=['GET'])
def get_device_time_added():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id'):
			ip_address = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				return jsonify({'result':device.get_time_added()})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_device_total_sensor', methods=['GET'])
def get_device_total_sensor():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id'):
			ip_address = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				return jsonify({'result':device.get_total_sensor()})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_device_sensor_list', methods=['GET'])
def get_device_sensor_list():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id'):
			ip_address = content['device_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				sensors = device.get_sensor_list()
				sensor_list = [{'sensor_id':x.get_sensor_id(),'sensor_name':x.get_sensor_name(),'time_added':x.get_time_added()} for x in sensors]
				return jsonify({'result':sensor_list})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/DEVICE-------------------------

#------------------SENSOR-------------------------
@app.route('/api/get_sensor_name', methods=['GET'])
def get_sensor_name():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id') and content.get('sensor_id'):
			ip_address = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					return jsonify({'result':sensor.get_sensor_name()})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' and/or 'sensor_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_time_added', methods=['GET'])
def get_sensor_time_added():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content.get('device_id') and content.get('sensor_id'):
			ip_address = content['device_id']
			sensor_id = content['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
						return jsonify({'result':sensor.get_time_added()})
				else:
						return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' and/or 'sensor_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_data', methods=['GET'])
def get_sensor_data():
	if session.get('logged_in') and session.get('email'):
		if request.args.get('device_id') and request.args.get('sensor_id') and request.args.get('from'):
			try:
				from_number = int(request.args['from'])
				assert from_number > 0
			except:
				return jsonify({'result':False, 'reason':"'from' must be a positive integer"})
			ip_address = request.args['device_id']
			sensor_id = request.args['sensor_id']
			user = iotku.find_user(email=session['email'])
			device = user.find_device(ip_address)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					data_collection = sensor.get_data(from_number,from_number+25)
					return jsonify({'result':data_collection})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry, 'sensor_id' entry, and/or 'from' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_total_data_entry', methods=['GET'])
def get_sensor_total_data_entry():
	if session.get('logged_in') and session.get('email'):
		if request.args.get('device_id') and request.args.get('sensor_id'):
			ip_address = request.args['device_id']
			sensor_id = request.args['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					total_entry = sensor.get_total_data_entry()
					return total_entry
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry and/or 'sensor_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_last_data_added_time', methods=['GET'])
def get_sensor_last_data_added_time():
	if session.get('logged_in') and session.get('email'):
		if request.args.get('device_id') and request.args.get('sensor_id'):
			ip_address = request.args['device_id']
			sensor_id = request.args['sensor_id']
			user = iotku.find_user(email=session["email"])
			device = user.find_device(ip_address)
			if device:
				sensor = device.find_sensor(sensor_id)
				if sensor:
					last_time = sensor.get_last_data_added_time()
					return last_time
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_id' entry and/or 'sensor_id' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/post', methods=['POST'])
def post_sensor_data():
	if session.get('api_key'):
		if request.is_json:
			content = request.get_json(silent=True)
			if 'data' in content.keys() and 'sensor_id' in content.keys():
				try:
					ip_address = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
					data = session['api_key'] + ' , ' + ip_address + ' , ' + content['sensor_id'] + ' , ' + content['data']
					c.publish(subject='post', payload=bytes(data, 'utf-8'))
					return jsonify({'result': True})
				except Exception as e:
					print('Error at post_sensor_data: ' + str(e))
					return jsonify({'result': False,'reason': 'Unexpected error. Try reconnecting to your account'})
			else:
				return jsonify({'result': False, 'reason': 'Make sure that \'data\' entry and \'sensor_id\' entry is in your JSON'})
		return jsonify({'result': False,'reason': "Invalid format"})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})
#------------------/SENSOR-------------------------

#---------------------MISC---------------------------
@app.route('/api/url', methods=['GET'])
def get_url_list():
	api_functions = [
						# CORE
						'connect',
						'disconnect',
						'is_logged_in',

						# USER
						'get_user_email',
						'get_user_api_key',
						'get_user_time_added',
						'get_user_total_device',
						'get_device_list',

						# DEVICE
						'get_device_name',
						'get_device_time_added',
						'get_device_total_sensor',
						'get_device_sensor_list',

						# SENSOR
						'get_sensor_name',
						'get_sensor_time_added',
						'get_sensor_data',
						'get_sensor_total_data_entry',
						'get_sensor_last_data_added_time',
						'post_sensor_data',

						# MISC
						'get_url_list'
					]
	api_functions_url = {x: url_for(x) for x in api_functions}
	return jsonify({'result':api_functions_url})
#---------------------/MISC---------------------------

#--------------------/API---------------------------


if __name__ == "__main__":
		app.secret_key = "secret key"
		app.run(debug=True,host='0.0.0.0', port=5000)
