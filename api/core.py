from flask import Blueprint, request, session, jsonify, url_for
from .iotku_database import Iotku
from . import api

iotku = Iotku()

#---------------------CORE---------------------------
@api.route('/api/register', methods=['POST'])
def register():
  content = request.get_json(silent=True)
  if all(x in content.keys() for x in ["email","password"]):
    email = content["email"]
    password = content["password"]
    if not iotku.find_user(email=email):
      user = iotku.add_user(email=email,password=password)
      session['logged_in'] = True
      session['email'] = user.get_email()
      session['api_key'] = user.get_api_key()
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
        device = user.find_device(device_id)
        if device: 
          session['logged_in'] = True
          session['api_key'] = user.get_api_key()
          session['device_id'] = device.get_device_id()
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
      session['email'] = user.get_email()
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