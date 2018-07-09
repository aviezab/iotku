from flask import Flask, request, session, render_template, url_for, redirect, jsonify
from redissession import RedisSessionInterface
import api, os

app = Flask(__name__, static_url_path='', static_folder='./frontend')
app.register_blueprint(api.api)
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()

@app.route("/", methods=['GET'])
def index():
	if session.get('logged_in') and session.get('email'):
		return redirect(url_for('dashboard'))
	else:
		return app.send_static_file('index.html')

@app.route("/dashboard")
def dashboard():
  if session.get('logged_in') and session.get('email'):
    return app.send_static_file('dashboard.html')
  else:
    return redirect(url_for('index'))

@app.route("/dashboard.html")
def dashboard_html():
  return redirect(url_for('dashboard'))

@app.route("/index.html")
def index_html():
  return redirect(url_for('index'))

@app.route("/api/url", methods=['GET'])
def site_map():
  links = dict()
  for rule in app.url_map.iter_rules():
    # Filter out rules we can't navigate to in a browser
    # and rules that require parameters
    if api.name in rule.endpoint:
      url = url_for(rule.endpoint, **(rule.defaults or {}))
      links[rule.endpoint[len(api.name)+1:]] = url
  # links is now a dictionary of url
  return jsonify({'result':links})

if __name__ == "__main__":
		app.secret_key = os.urandom(24)
		app.run(host='0.0.0.0', port=5000)