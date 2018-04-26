from flask import Flask, request, session, render_template, url_for, redirect
from redissession import RedisSessionInterface
from iotku_database import Iotku
from api.views import api
import os, hashlib

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(api)
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
		else:
			return jsonify({'result': False,'reason':'An account with the same email exists'})
	else: 
		return jsonify({'result': False,'reason':'Invalid format'})

@app.route('/device', methods=['GET'])
def device_list():
	if session.get('logged_in') and session.get('email'):
		return render_template('device.html')
	else:
		return redirect(url_for('index'))

@app.route('/device/<device_id>', methods=['GET'])
def device(device_id):
	if session.get('logged_in') and session.get('email'):
		return render_template('device.html')
	else:
		return redirect(url_for('index'))

if __name__ == "__main__":
		app.secret_key = "secret key"
		app.run(debug=True,host='0.0.0.0', port=5000)
