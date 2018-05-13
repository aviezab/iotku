from flask import Blueprint, request, session, jsonify, url_for
from .iotku_database import Iotku
from . import api

iotku = Iotku()

#-------------------RULE-------------------------
@api.route('/api/rule/name', methods=['GET'])
def rule_name():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result': False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('rule_name')})

@api.route('/api/rule/expected_type', methods=['GET'])
def rule_expected_type():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('expected_type')})

@api.route('/api/rule/condition', methods=['GET'])
def rule_condition():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('condition')})

@api.route('/api/rule/endpoint', methods=['GET'])
def rule_endpoint():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('endpoint')})

@api.route('/api/rule/command', methods=['GET'])
def rule_command():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('command')})

@api.route('/api/rule/time_added', methods=['GET'])
def rule_time_added():
  content = request.args
  if not all(x in session.keys() for x in ["logged_in","email"]):
    return jsonify({'result':False,'reason':'Not logged in / Unauthorized'})
  elif not all(x in content.keys() for x in ["device_id","sensor_id","rule_id"]):
    return jsonify({'result': False, 'reason': 'Invalid format'})
  else:
    device_id = content['device_id']
    sensor_id = content['sensor_id']
    rule_id = content["rule_id"]
    user = iotku.find_user(email=session["email"])
    device = user.find_device(device_id)
    if not device:
      return jsonify({'result': False, 'reason': "Device ID not found"})
    else:
      sensor = device.find_sensor(sensor_id)
      if not sensor:
        return jsonify({'result': False, 'reason': "Sensor ID not found"})
      else:
        rule = sensor.find_rule(rule_id)
        if not rule:
          return jsonify({'result': False, 'reason': "Rule ID not found"})
        else:
          return jsonify({'result': rule.get('time_added')})
#------------------/RULE-------------------------