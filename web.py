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
def do_register():
    if request.form['password'] and request.form['email']:
        db = client['iotku']
        collection = db['user']
        if not collection.find_one({"email":request.form['email']}):
            collection.insert_one({"email":request.form['email'],
                                "password":request.form['password'],
                                "api_key":hashlib.md5(request.form['email'].encode('utf-8')).hexdigest(),
                                "device":{}
                                })
            session['logged_in'] = True
            session['email'] = request.form['email']
    return redirect(url_for('index'))

@app.route('/device', methods=['GET'])
def device():
    if session.get('logged_in') and session.get('email') and request.args.get('device_ip'):
        if request.args.get('device_ip') in client['iotku']['user'].find_one({'email':session['email']})['device']:
            return render_template('device.html', username=session.get('email'), device=[[client['iotku']['user'].find_one({'email':session['email']})['device'][x]['deviceName'],x] for x in client['iotku']['user'].find_one({'email':session['email']})['device'].keys()], sensor=[[x,client['iotku']['device_data'].find_one({'_id':client['iotku']['user'].find_one({'email':session['email']})['device'][request.args.get('device_ip')]['id']})['sensorList'][x]['time_added']] for x in client['iotku']['device_data'].find_one({'_id':client['iotku']['user'].find_one({'email':session['email']})['device'][request.args.get('device_ip')]['id']})['sensorList']])
        else:
            return render_template('devicenotfound.html', username=session['email'])
    else:
        return redirect(url_for('index'))
		
@app.route('/api/connect', methods=['POST'])
def do_login():
	if request.is_json:
		content = request.get_json(silent=True)
		if 'api_key' in content.keys():
			try:
				collection = client['iotku']['user']
				api_key = content['api_key']
				ip_address = request.environ.get('HTTP_X_REAL_IP',request.remote_addr)
				doc = collection.find_one({'api_key':api_key})
				if doc:
					if not ip_address in doc['device'].keys():
						mongoid = db['device_data'].insert({'sensorList':{}})
						doc['device'][ip_address] = {'deviceName':ip_address,'id':mongoid}
						collection.save(doc)
					result = True
				else:
					result = False
			except Exception as e:
				print('Unknown error at do_login: ' + str(e))
				reason = 'Unknown Error'
				return jsonify({'result': False, 'reason': reason})
			if result:
				session['api_key'] = content['api_key']
				return jsonify({'result': True})
			else:
				reason = 'Failed'
				return jsonify({'result': False,'reason': reason})
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
				return jsonify({'result': False})
	elif request.form['password'] and request.form['email']:
		db = client['iotku']
		collection = db['user']
		doc = collection.find_one({"email":request.form['email'],"password":request.form['password']})
		if doc:
			session['logged_in'] = True
			session['api_key'] = doc['api_key']
			session['email'] = request.form['email']
		return redirect(url_for('index'))
	return jsonify({'result': False,'reason': "Invalid format"})

@app.route('/api/disconnect')
def do_logout():
	#Membuang session. {dev aviezab 2018.03.08}
	session.pop('email', None)
	session.pop('api_key', None)
	session['logged_in'] = False
	if request.method == 'POST': return redirect(url_for('index'))
	else: return jsonify({'result': True})

@app.route('/api/is_logged_in')
def is_logged_in():
	if session.get('logged_in'):
		return jsonify({'result': True})
	else: return jsonify({'result': False})
	
#------------------POST Data------------------------
@app.route('/api/post', methods=['POST'])
def post_data():
	if session.get('api_key'):
		content = request.get_json(silent=True)
		if 'data' in content.keys() and 'sensorId' in content.keys():
			try:
				c.publish(subject='post', payload=bytes(session['api_key'] + ' , ' + request.environ.get('HTTP_X_REAL_IP',request.remote_addr) + ' , ' + content['sensorId'] + ' , ' + content['data'], 'utf-8'))
				return jsonify({'result': True})
			except Exception as e:
				print('Error at post_data: ' + str(e))
				return jsonify({'result': False,'reason': 'Unexpected error. Try reconnecting to your account.'})
		else: return jsonify({'result': False, 'reason': 'Make sure that \'data\' entry and \'sensorId\' entry is in your JSON.'})
	else: return jsonify({'result': False, 'reason': 'Not connected to any account.'})
#------------------/POST Data------------------------



#------------------GET Data-------------------------
@app.route('/api/logged_in_email', methods=['GET'])
def get_logged_in_email():
	if session.get('logged_in') and session.get('email'):
		return jsonify({'result': session['email']})
	else: return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
	
@app.route('/api/logged_in_api_key', methods=['GET'])
def get_logged_in_api_key():
	if session.get('logged_in') and session.get('api_key'):
		return jsonify({'result': session['api_key']})
	else: return jsonify({'result':False,'reason':'Not connected to any account.'})
	
@app.route('/api/get_device_list', methods=['GET'])
def get_device_list():
	if session.get('logged_in') and session.get('email'):
		db = client['iotku']
		device_ip = [x for x in db['user'].find_one({'email':session['email']})['device'].keys()]
		device_name = [db['user'].find_one({'email':session['email']})['device'][x]['deviceName'] for x in device_ip]
		return jsonify({'result':[list(x) for x in zip(device_ip, device_name)]})
	else: return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_list', methods=['GET'])
def get_sensor_list():
	content = request.args
	if session.get('logged_in') and session.get('email'):
		if content['device_ip']:
			ip_address = content['device_ip']
			db = client['iotku']
			collection = db['user']
			doc = collection.find_one({'email':session['email']})
			if ip_address in doc['device'].keys():
				sensorName = [x for x in db['device_data'].find_one({'_id':doc['device'][ip_address]['id']})['sensorList'].keys()]
				sensorDate = [db['device_data'].find_one({'_id':doc['device'][ip_address]['id']})['sensorList'][x]['time_added'] for x in sensorName]
				sensorList = [list(x) for x in zip(sensorName, sensorDate)]
				return jsonify({'result':sensorList})
			else: return jsonify({'result':False,'reason':'Device IP not found'})
		else: return jsonify({'result':False,'reason':"'device_ip' entry not found in JSON"})
	else: return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})

@app.route('/api/get_sensor_data', methods=['GET'])
def get_sensor_data():
	if session.get('logged_in') and session.get('email'):
		if request.args.get('device_ip') and request.args.get('sensorId') and request.args.get('from'):
			try:
				from_number = int(request.args['from'])
			except:
				return jsonify({'result':False, 'reason':"'from' must be integer"})
			ip_address = request.args['device_ip']
			sensor_id = request.args['sensorId']
			db = client['iotku']
			collection = db['user']
			doc = collection.find_one({'email':session['email']})
			if ip_address in doc['device'].keys():
				data_doc = db['device_data'].find_one({'_id':doc['device'][ip_address]['id']})
				if sensor_id in data_doc['sensorList']:
					time_added = list(data_doc['sensorList'][sensor_id]['data'].keys())[from_number:from_number+25]
					data = [data_doc['sensorList'][sensor_id]['data'][x] for x in time_added]
					return jsonify({'result':{time_added[x]: data[x] for x in range(25) if x < len(time_added)}})
				else: return jsonify({'result':False,'reason':'Sensor ID not found'})
			else: return jsonify({'result':False, 'reason':'IP not found'})
		else: return jsonify({'result':False,'reason':"'device_ip' entry, 'sensorId' entry, and/or 'from' entry not found in query"})
	else: return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
#------------------/GET Data------------------------

if __name__ == "__main__":
    app.secret_key = "secret key"
    app.run(debug=True,host='0.0.0.0', port=5000)
