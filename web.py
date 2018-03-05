from flask import *
from pymongo import MongoClient
import os

client = MongoClient()
app = Flask(__name__, static_url_path='/static')

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

@app.route('/register', methods=['POST'])
def do_register():
    if request.form['password'] and request.form['email']:
        db = client['iotku']
        collection = db['user']
        if not collection.find_one({"email":request.form['email']}) and not collection.find_one({"ip":request.remote_addr}):
            collection.insert_one({"email":request.form['email'],"password":request.form['password'],"ip":request.environ.get('HTTP_X_REAL_IP', request.remote_addr)})
        session['logged_in'] = True
        session['email'] = request.form['email']
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=5000)
