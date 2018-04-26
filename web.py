from flask import Flask, request, session, render_template, url_for, redirect
from redissession import RedisSessionInterface
from api import views
import os, hashlib

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(views.api)
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()

@app.route("/", methods=['GET'])
def index():
	if session.get('logged_in') and session.get('email'):
		return render_template('dashboard.html')
	else:
		return render_template('index.html', api_connect=url_for(views.api.connect.__name__), api_register=url_for(views.api.register.__name__))

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
