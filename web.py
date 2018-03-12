from flask import *
from pymongo import MongoClient
import os
from redissession import RedisSessionInterface
import hashlib

client = MongoClient()
app = Flask(__name__, static_url_path='/static')
#Session akan disimpan pada RAM ketimbang Harddisk sehingga performa meningkat
app.session_interface = RedisSessionInterface()

@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('dashboard.html', username=session.get('email'))

@app.route('/login', methods=['POST'])
def do_login():
    if request.form['password'] and request.form['email']:
        db = client['iotku']
        collection = db['user']
        if collection.find_one({"email":request.form['email'],"password":request.form['password']}):
            session['logged_in'] = True
            session['email'] = request.form['email']
        else:
            flash('wrong password!')
    return redirect(url_for('index'))

@app.route('/logout')
def do_logout():
   #Membuang session. {dev aviezab 2018.03.08}
   session.pop('email', None)
   session['logged_in'] = False
   return redirect(url_for('index'))


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

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
