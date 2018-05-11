from flask import Blueprint, request, session, jsonify, url_for
from .iotku_database import Iotku
from . import api

iotku = Iotku()

#------------------DEVICE-------------------------

@api.route('/api/device/name', methods=['GET'])
def device_name():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not content.get('device_id'):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      return jsonify({'result':device.get_device_name()})

@api.route('/api/device/time_added', methods=['GET'])
def device_time_added():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not content.get('device_id'):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      return jsonify({'result':device.get_time_added()})

@api.route('/api/device/total_sensor', methods=['GET'])
def device_total_sensor():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not content.get('device_id'):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      return jsonify({'result':device.get_total_sensor()})
      

@api.route('/api/device/sensor_list', methods=['GET'])
def device_sensor_list():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not content.get('device_id'):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensors = device.get_sensor_list()
      sensor_id = [x.get_sensor_id() for x in sensors]
      sensor_name = [x.get_sensor_name() for x in sensors]
      sensor_list = [{'sensor_id':x,'sensor_name':y} for x,y in zip(sensor_id, sensor_name)]
      return jsonify({'result':sensor_list})

@api.route('/api/device/add_sensor', methods=['POST'])
def device_add_sensor():
  content = request.get_json(silent=True)
  if not content:
    return jsonify({'result': False, 'reason': 'Invalid format'})
  elif not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","sensor_name"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor_id, sensor_name = content["sensor_id"],content["sensor_name"]
      if device.find_sensor(sensor_id):
        return jsonify({'result': False, 'reason': "Sensor ID exists"})
      else:
        device.add_sensor(sensor_id,sensor_name)
        return jsonify({'result': True})

@api.route('/api/device/remove_sensor', methods=['POST'])
def device_remove_sensor():
  content = request.get_json(silent=True)
  if not content:
    return jsonify({'result': False, 'reason': 'Invalid format'})
  elif not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor_id = content["sensor_id"]
      if device.find_sensor(sensor_id):
        device.remove_sensor(sensor_id)
        return jsonify({'result': True})
      else:
        return jsonify({'result': False, 'reason': "Sensor not found"})

@api.route('/api/device/command', methods=['GET'])
def device_command():
  content = request.args
  if not 'device_id' in content.keys():
    if not all(x in session.keys() for x in ["logged_in","device_id"]):
      return jsonify({'result':False,'reason':'Not logged in / Invalid login type / Invalid format'})
    else:
      device_id = session['device_id']
      user = iotku.find_user(api_key=session["api_key"])
      device = user.find_device(device_id)
      if not device:
        return jsonify({'result': False, 'reason': "Invalid Device ID. Please relogin"})
      else:
        command = device.get_command()
        return jsonify({'result': command})
  else:
    if not all(x in session.keys() for x in ["logged_in","email"]):
      return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
    else:
      device_id = content['device_id']
      user = iotku.find_user(email=session["email"])
      device = user.find_device(device_id)
      if not device:
        return jsonify({'result': False, 'reason': "Invalid Device ID"})
      else:
        command = device.get_command()
        return jsonify({'result': command})

@api.route('/api/device/command_history', methods=['GET'])
def device_command_history():
  content = request.args
  if not 'device_id' in content.keys():
    if not all(x in session.keys() for x in ["logged_in","device_id"]):
      return jsonify({'result':False,'reason':'Not logged in / Invalid login type / Invalid format'})
    else:
      device_id = session['device_id']
      user = iotku.find_user(api_key=session["api_key"])
      device = user.find_device(device_id)
      if not device:
        return jsonify({'result': False, 'reason': "Invalid Device ID. Please relogin"})
      else:
        command = device.get_command_history()
        return jsonify({'result': command})
  else:
    if not all(x in session.keys() for x in ["logged_in","email"]):
      return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
    else:
      device_id = content['device_id']
      user = iotku.find_user(email=session["email"])
      device = user.find_device(device_id)
      if not device:
        return jsonify({'result': False, 'reason': "Invalid Device ID"})
      else:
        command = device.get_command_history()
        return jsonify({'result': command})

#------------------/DEVICE-------------------------