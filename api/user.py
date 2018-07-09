from flask import Blueprint, request, session, jsonify, url_for
from . import api, iotku

#------------------USER-------------------------
@api.route('/api/user/email', methods=['GET'])
def user_email():
  if not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  else:
    return jsonify({'result': session['email']})

@api.route('/api/user/api_key', methods=['GET'])
def user_api_key():
  if not all(x in session.keys() for x in ["logged_in","api_key"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not connected to any account.'})
  else:
    return jsonify({'result': session['api_key']})

@api.route('/api/user/time_added', methods=['GET'])
def user_time_added():
  if not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  else:
    user = iotku.find_user(email=session["email"])
    return jsonify({'result':user.get('time_added')})

@api.route('/api/user/total_device', methods=['GET'])
def user_total_device():
  if not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  else:
    user = iotku.find_user(email=session["email"])
    return jsonify({'result': user.get('total_device')})

@api.route('/api/user/device_list', methods=['GET'])
def user_device_list():
  if not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  else:
    user = iotku.find_user(email=session["email"])
    devices = user.get_device_list()
    device_id = [x.get('device_id') for x in devices]
    device_name = [x.get('device_name') for x in devices]
    device_list = [{'device_id':x,'device_name':y} for x,y in zip(device_id,device_name)]
    return jsonify({'result':device_list})

@api.route('/api/user/add_device', methods=['POST'])
def user_add_device():
  content = request.get_json(silent=True)
  if not content:
    # If not JSON
    return jsonify({'result': False, 'reason': 'Invalid format'})
  elif not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","device_name"]):
    # If JSON is in incorrect format
    return jsonify({'result': False, 'reason': 'Invalid format'})
  elif not content['device_id'] or not content['device_name']:
    # If device_id and/or device_name is empty
    return jsonify({'result': False, 'reason': "Device ID and/or device name cannot be empty"})
  else:    
    device_id = content['device_id']
    device_name = content['device_name']
    user = iotku.find_user(email=session["email"])
    if not user.find_device(device_id):
      user.add_device(device_id,device_name)
      return jsonify({'result': True})
    else:
      return jsonify({'result': False, 'reason': "Device ID exists"})

@api.route('/api/user/remove_device', methods=['POST'])
def user_remove_device():
  content = request.get_json(silent=True)
  if not content:
    # If not JSON
    return jsonify({'result': False, 'reason': 'Invalid format'})
  elif not all(x in session.keys() for x in ["logged_in","email"]):
    # If not logged in as user
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id"]):
    # If JSON is in incorrect format
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    if user.find_device(device_id):
      user.remove_device(device_id)
      return jsonify({'result': True})
    else:
      return jsonify({'result': False, 'reason': "Device ID not found"})
#------------------/USER-------------------------

