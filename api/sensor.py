from flask import Blueprint, request, session, jsonify, url_for
from . import api, iotku, c

#------------------SENSOR-------------------------
@api.route('/api/sensor/name', methods=['GET'])
def sensor_name():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        return jsonify({'result':sensor.get('sensor_name')})

@api.route('/api/sensor/time_added', methods=['GET'])
def sensor_time_added():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        return jsonify({'result':sensor.get('time_added')})

@api.route('/api/sensor/get_data', methods=['GET'])
def sensor_get_data():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    try:
      from_number = int(content['from'])
      assert from_number >= 0
    except:
      from_number = 0
    try:
      to_number = int(content['to'])
      assert from_number < to_number and to_number < 25
    except:
      to_number = from_number + 25
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session['email'])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False, 'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        data_collection = sensor.get_data(from_number,to_number)
        return jsonify({'result':data_collection})

@api.route('/api/sensor/total_data_entry', methods=['GET'])
def sensor_total_data_entry():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        return jsonify({'result':sensor.get('total_data_entry')})

@api.route('/api/sensor/last_data_added_time', methods=['GET'])
def sensor_last_data_added_time():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        return jsonify({'result':sensor.get('last_data_added_time')})

@api.route('/api/sensor/post_data', methods=['POST'])
def sensor_post_data():
  content = request.get_json(silent=True)
  if not all(x in session.keys() for x in ["logged_in","api_key","device_id"]):
    return jsonify({'result': False, 'reason': 'Not connected to any account / Invalid login type'})
  elif not all(x in content.keys() for x in ["data","sensor_id"]):
    return jsonify({'result': False,'reason': "Invalid format"})
  else:
    data = str(content['data'])
    device_id = session['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(api_key=session['api_key'])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False, 'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        formatted = session['api_key'].encode("ascii").hex() + ' , ' + device_id.encode("ascii").hex() + ' , ' + sensor_id.encode("ascii").hex() + ' , ' + data.encode("ascii").hex()
        c.publish(subject='post', payload=bytes(formatted, 'utf-8'))
        return jsonify({'result': True})

@api.route('/api/sensor/total_rule', methods=['GET'])
def sensor_total_rule():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        return jsonify({'result':sensor.get('total_rule')})

@api.route('/api/sensor/rule_list', methods=['GET'])
def sensor_rule_list():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id"]):
    return jsonify({'result':False,'reason':"Invalid format"})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result':False,'reason':'Device ID not found'})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result':False,'reason':'Sensor ID not found'})
      else:
        rules = sensor.get_rule_list()
        rule_id = [x.get('rule_id') for x in rules]
        rule_name = [x.get('rule_name') for x in rules]
        rule_list = [{'rule_id':x,'rule_name':y} for x,y in zip(rule_id, rule_name)]
        return jsonify({'result':rule_list})


@api.route('/api/sensor/add_rule', methods=['POST'])
def sensor_add_rule():
  content = request.get_json(silent=True)
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id","rule_name","expected_type","condition","endpoint","command"]):
    return jsonify({'result': False, 'reason': "Invalid format"})
  elif not content['expected_type'].upper() in ['STR','INT']:
    return jsonify({'result': False, 'reason': "Invalid expected_type"})
  else:
    try:
      for x in content['condition']:
        assert x['operator'] in ['EQU','NEQ','LSS','LEQ','GTR','GEQ']
        if content['expected_type'].upper() == 'STR':
          x['value'] = str(x['value'])
        elif content['expected_type'].upper() == 'INT':
          x['value'] = int(x['value'])
    except Exception as e:
      print(str(e))
      return jsonify({'result': False, 'reason': "Invalid format for one of the conditions"})

    device_id = content['device_id']
    sensor_id = content['sensor_id']
    endpoint = content["endpoint"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device or not user.find_device(endpoint):
      return jsonify({'result': False, 'reason': "Device ID and/or Endpoint not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule_id = content["rule_id"]
        rule_name = content["rule_name"]
        expected_type = content["expected_type"]
        condition = content["condition"]
        command = content["command"]
        if sensor.find_rule(rule_id):
          return jsonify({'result': False, 'reason': "Rule ID exists"})
        else:
          sensor.add_rule(rule_id,rule_name,expected_type,condition,endpoint,command)
          return jsonify({'result': True})

@api.route('/api/sensor/remove_rule', methods=['POST'])
def sensor_remove_rule():
  content = request.get_json(silent=True)
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule_id = content["rule_id"]
        if not sensor.find_rule(rule_id):
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          sensor.remove_rule(rule_id)
          return jsonify({'result': True})

#------------------/SENSOR-------------------------