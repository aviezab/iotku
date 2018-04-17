from flask import *
from pymongo import MongoClient
from redissession import RedisSessionInterface
import os, hashlib

client = MongoClient()
app = Flask(__name__, static_url_path='/static')
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()

@app.route("/", methods=['GET'])
def index():
	if session.get('logged_in') and session.get('email'):
		return render_template('dashboard.html')
	else: 
		return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
	if request.form['password'] and request.form['email']:
		db = client['iotku']
		collection = db['user']
		if not collection.find_one({"email":request.form['email']}):
			collection.insert_one({"email":request.form['email'],
								"password":request.form['password'],
								"api_key":hashlib.md5(request.form['email'].encode('utf-8')).hexdigest(),
								"device_list":{}
								})
			session['logged_in'] = True
			session['email'] = request.form['email']
			session['api_key'] = hashlib.md5(request.form['email'].encode('utf-8')).hexdigest()
			return jsonify({'result': True})
		return jsonify({'result': False,'reason':'An account with the same email exists'})
	return jsonify({'result': False,'reason':'Invalid format'})

@app.route('/device', methods=['GET'])
def device():
	if session.get('logged_in') and session.get('email'):
		return render_template('device.html')
	else:
		return redirect(url_for('index'))
		
#---------------------API---------------------------
@app.route('/api/connect', methods=['POST'])
def connect():
	if request.is_json:
		content = request.get_json(silent=True)
		if 'api_key' in content.keys():
			try:
				collection = client['iotku']['user']
				api_key = content['api_key']
				ip_address = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
				doc = collection.find_one({'api_key':api_key})
				if doc:
					if not ip_address in doc['device_list'].keys():
						mongo_id = db['device_data'].insert({'sensor_list':{}})
						doc['device_list'][ip_address] = {'device_name':ip_address,'id':mongo_id}
						collection.save(doc)
					session['api_key'] = content['api_key']
					return jsonify({'result': True})
				else:
					return jsonify({'result': False,'reason': 'Invalid API key'})
			except Exception as e:
				print('Unknown error at do_login: ' + str(e))
				return jsonify({'result': False, 'reason': 'Unknown Error'})
		elif 'email' in content.keys() and 'password' in content.keys():
			email = content['email']
			password = content['password']
			db = client['iotku']
			collection = db['user']
			doc = collection.find_one({"email":email,"password":password})
			if doc:
				session['logged_in'] = True
				session['api_key'] = doc['api_key']
				session['email'] = request.form['email']
				return jsonify({'result': True})
			else:
				return jsonify({'result': False,'reason':'Wrong email or password'})
	return jsonify({'result': False,'reason': "Invalid format"})

@app.route('/api/disconnect')
def disconnect():
	#Membuang session. {dev aviezab 2018.03.08}
	session.pop('email', None)
	session.pop('api_key', None)
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
	
#------------------POST Data------------------------
@app.route('/api/post', methods=['POST'])
def post_data():
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
					print('Error at post_data: ' + str(e))
					return jsonify({'result': False,'reason': 'Unexpected error. Try reconnecting to your account'})
			else:
				return jsonify({'result': False, 'reason': 'Make sure that \'data\' entry and \'sensor_id\' entry is in your JSON'})
		return jsonify({'result': False,'reason': "Invalid format"})
	else:
		return jsonify({'result': False, 'reason': 'Not connected to any account'})
#------------------/POST Data------------------------



#------------------GET Data-------------------------
@app.route('/api/logged_in_email', methods=['GET'])
def get_logged_in_email():
	if session.get('logged_in') and session.get('email'):
		return jsonify({'result': session['email']})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
	
@app.route('/api/logged_in_api_key', methods=['GET'])
def get_logged_in_api_key():
	if session.get('logged_in') and session.get('api_key'):
		return jsonify({'result': session['api_key']})
	else:
		return jsonify({'result':False,'reason':'Not connected to any account.'})
	
@app.route('/api/get_device_list', methods=['GET'])
def get_device_list():
	if session.get('logged_in') and session.get('email'):
		db = client['iotku']
		doc = db['user'].find_one({'email':session['email']})
		device_ip = [x for x in doc['device_list'].keys()]
		device_name = [doc['device_list'][x]['device_name'] for x in device_ip]
		device_list = [{'device_ip':list(x)[0],'device_name':list(x)[1]} for x in zip(device_ip, device_name)]
		return jsonify({'result':device_list})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_list', methods=['GET'])
def get_sensor_list():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content['device_ip']:
			ip_address = content['device_ip']
			db = client['iotku']
			collection = db['user']
			doc = collection.find_one({'email':session['email']})
			if ip_address in doc['device_list'].keys():
				data_doc = db['device_data'].find_one({'_id':doc['device_list'][ip_address]['id']})
				sensor_name = [x for x in data_doc['sensor_list'].keys()]
				sensor_date = [data_doc['sensor_list'][x]['time_added'] for x in sensor_name]
				sensor_list = [{'sensor_name':list(x)[0],'sensor_date':list(x)[1]} for x in zip(sensor_name, sensor_date)]
				return jsonify({'result':sensor_list})
			else:
				return jsonify({'result':False,'reason':'Device IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_ip' entry not found in JSON"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_data', methods=['GET'])
def get_sensor_data():
	if session.get('logged_in') and session.get('email'):
		if request.args.get('device_ip') and request.args.get('sensor_id') and request.args.get('from'):
			try:
				from_number = int(request.args['from'])
			except:
				return jsonify({'result':False, 'reason':"'from' must be integer"})
			ip_address = request.args['device_ip']
			sensor_id = request.args['sensor_id']
			db = client['iotku']
			collection = db['user']
			doc = collection.find_one({'email':session['email']})
			if ip_address in doc['device_list'].keys():
				data_doc = db['device_data'].find_one({'_id':doc['device_list'][ip_address]['id']})
				if sensor_id in data_doc['sensor_list']:
					time_added = list(data_doc['sensor_list'][sensor_id]['data'].keys())[from_number:from_number+25]
					data = [data_doc['sensor_list'][sensor_id]['data'][x] for x in time_added]
					return jsonify({'result':{time_added[x]: data[x] for x in range(len(time_added))}})
				else:
					return jsonify({'result':False,'reason':'Sensor ID not found'})
			else:
				return jsonify({'result':False, 'reason':'IP not found'})
		else:
			return jsonify({'result':False,'reason':"'device_ip' entry, 'sensor_id' entry, and/or 'from' entry not found in query"})
	else:
		return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

# @app.route('/api/get_sensor_data', methods=['GET'])
# def get_sensor_data():
	# if session.get('logged_in') and session.get('email'):
		# if request.args.get('device_ip') and request.args.get('sensor_id'):
			# ip_address = request.args['device_ip']
			# sensor_id = request.args['sensor_id']
			# db = client['iotku']
			# collection = db['user']
			# doc = collection.find_one({'email':session['email']})
			# if ip_address in doc['device_list'].keys():
				# data_doc = db['device_data'].find_one({'_id':doc['device_list'][ip_address]['id']})
				# if sensor_id in data_doc['sensor_list']:
					# total_data = len(
		# else:
			# return jsonify({'result':False,'reason':"'device_ip' entry and/or 'sensor_id' entry not found in query"})
	# else:
		# return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/GET Data------------------------

@app.route('/api/url', methods=['GET'])
def get_url_list():
	api_functions = [
						'connect',
						'disconnect',
						'is_logged_in',
						'get_logged_in_api_key',
						'get_logged_in_email',
						'post_data',
						'get_device_list',
						'get_sensor_list',
						'get_sensor_data',
						'get_sensor_data_total',
						'get_url_list'
					]
	api_functions_url = {x: url_for(x) for x in api_functions}
	return jsonify({'result':api_functions_url})

#--------------------/API---------------------------

	
if __name__ == "__main__":
    app.secret_key = "secret key"
    app.run(debug=True,host='0.0.0.0', port=5000)
