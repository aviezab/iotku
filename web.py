from flask import Flask, request, session, render_template, url_for, redirect
from redissession import RedisSessionInterface
import api

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(api.api)
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()

@app.route("/", methods=['GET'])
def index():
	if session.get('logged_in') and session.get('email'):
		return render_template('dashboard.html')
	else:
		return render_template('index.html')

if __name__ == "__main__":
		app.secret_key = "secret key"
		app.run(debug=True,host='0.0.0.0', port=5000)