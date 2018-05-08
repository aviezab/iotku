from pymongo import MongoClient
import hashlib, datetime

class Iotku:
  def __init__(
          self,
          client = MongoClient(),
          db = 'iotku',
          user_list = 'user_list',
          device_list = 'device_list',
          sensor_list = 'sensor_list',
          rule_list = 'rule_list'
        ):
    self.client = client
    self.db = self.client[db]
    self.user_list = self.db[user_list]
    self.device_list = self.db[device_list]
    self.sensor_list = self.db[sensor_list]
    self.rule_list = self.db[rule_list]

  def get_user_list(self):
    return_list = [User(x['_id'], self.user_list, self.device_list, self.sensor_list, self.rule_list) for x in self.user_list.find({})]
    return return_list

  def find_user(self, **user_info):
    result = self.user_list.find_one(user_info)
    if result:
      _id = result["_id"]
      return User(_id, self.user_list, self.device_list, self.sensor_list, self.rule_list)
    else:
      return False

  def add_user(self, email, password):
    if not self.find_user(email=email):
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      doc = {
              'email': email,
              'password': password,
              'api_key': hashlib.md5(email.encode('ascii')).hexdigest(),
              'time_added': date,
              'total_device': 0
            }
      inserted = self.user_list.insert_one(doc)
      _id = inserted.inserted_id
      return User(_id, self.user_list, self.device_list, self.sensor_list, self.rule_list)
    else:
      return False

class User(Iotku):
  def __init__(self, _id, user_list, device_list, sensor_list, rule_list):
    self.user_list = user_list
    self.device_list = device_list
    self.sensor_list = sensor_list
    self.rule_list = rule_list

    self._id = _id
    self.user_document = self.user_list.find_one({"_id":self._id})

  def change_user_info(self, **user_info):
    self.user_document = self.user_list.find_one({"_id":self._id})
    for key, value in user_info.iteritems():
      self.user_document[key] = value
    self.user_list.save(self.user_document)
    return True

  def get_email(self):
    self.user_document = self.user_list.find_one({"_id":self._id})
    return self.user_document["email"]

  def get_password(self):
    self.user_document = self.user_list.find_one({"_id":self._id})
    return self.user_document["password"]

  def get_api_key(self):
    self.user_document = self.user_list.find_one({"_id":self._id})
    return self.user_document["api_key"]

  def get_time_added(self):
    self.user_document = self.user_list.find_one({"_id":self._id})
    return self.user_document["time_added"]

  def get_total_device(self):
    self.user_document = self.user_list.find_one({"_id":self._id})
    return self.user_document["total_device"]

  def get_device_list(self):
    device_list = [Device(x["_id"],self.device_list,self.sensor_list, self.rule_list) for x in self.device_list.find({"api_key":self.get_api_key()})]
    return device_list

  def find_device(self, device_id):
    device_info = self.device_list.find_one({"device_id":device_id,"api_key":self.get_api_key()})
    if device_info:
      _id = device_info["_id"]
      return Device(_id, self.device_list, self.sensor_list, self.rule_list)
    else:
      return False

  def add_device(self, device_id, device_name):
    if not self.find_device(device_id):
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      mongo_id = self.device_list.insert_one({
                      "api_key":self.get_api_key(),
                      "device_id":device_id,
                      "device_name":device_name,
                      "total_sensor":0,
                      "time_added":date
                      })
      self.user_document = self.user_list.find_one({"_id":self._id})
      self.user_document["total_device"] += 1
      self.user_list.save(self.user_document)
      _id = mongo_id.inserted_id
      return Device(_id, self.device_list, self.sensor_list, self.rule_list)
    else:
      return False

  def remove_device(self, device_id):
    device_info = self.find_device(device_id)
    if device_info:
      self.device_list.remove({"_id":device_info._id})
      self.user_document = self.user_list.find_one({"_id":self._id})
      self.user_document["total_device"] -= 1
      self.user_list.save(self.user_document)
      self.sensor_list.remove({"api_key":self.get_api_key(),"device_id":device_id})
      return True
    else:
      return False

class Device(User):
  def __init__(self, _id, device_list, sensor_list, rule_list):
    self.device_list = device_list
    self.sensor_list = sensor_list
    self.rule_list = rule_list
    self._id = _id
    self.device_document = self.device_list.find_one({"_id":self._id})

  def get_device_name(self):
    self.device_document = self.device_list.find_one({"_id":self._id})
    return self.device_document["device_name"]

  def get_device_id(self):
    self.device_document = self.device_list.find_one({"_id":self._id})
    return self.device_document["device_id"]

  def get_time_added(self):
    self.device_document = self.device_list.find_one({"_id":self._id})
    return self.device_document["time_added"]

  def get_total_sensor(self):
    self.device_document = self.device_list.find_one({"_id":self._id})
    return self.device_document["total_sensor"]

  def get_api_key(self):
    self.device_document = self.device_list.find_one({"_id":self._id})
    return self.device_document["api_key"]

  def change_device_info(self, **device_info):
    self.device_document = self.device_list.find_one({"_id":self._id})
    for key, value in device_info.iteritems():
      self.device_document[key] = value
      self.device_list.save(self.device_document)
    return True

  def get_sensor_list(self):
    sensor_list = [Sensor(x["_id"],self.sensor_list,self.rule_list) for x in self.sensor_list.find({"api_key":self.get_api_key(),"device_id":self.get_device_id()})]
    return sensor_list

  def find_sensor(self, sensor_id):
    sensor_info = self.sensor_list.find_one({"device_id":self.get_device_id(),"api_key":self.get_api_key(),"sensor_id":sensor_id})
    if sensor_info:
      _id = sensor_info["_id"]
      return Sensor(_id, self.sensor_list,self.rule_list)
    else:
      return False

  def add_sensor(self, sensor_id, sensor_name):
    if not self.find_sensor(sensor_id):
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      mongo_id = self.sensor_list.insert_one({
          "api_key":self.get_api_key(),
          "device_id":self.get_device_id(),
          "sensor_id":sensor_id,
          "sensor_name":sensor_name,
          "last_data_added_time":"Never",
          "total_data_entry":0,
          "total_rule":0,
          "data_collection":[],
          "time_added":date
        })
      _id = mongo_id.inserted_id
      self.device_document = self.device_list.find_one({"_id":self._id})
      self.device_document["total_sensor"] += 1
      self.device_list.save(self.device_document)
      return Sensor(_id, self.sensor_list,self.rule_list)
    else:
      return False

  def remove_sensor(self, sensor_id):
    sensor_info = self.find_sensor(sensor_id)
    if sensor_info:
      self.sensor_list.remove({"_id":sensor_info._id})
      self.device_document = self.device_list.find_one({"_id":self._id})
      self.device_document["total_sensor"] -= 1
      self.device_list.save(self.device_document)
      return True
    else:
      return False

class Sensor(Device):
  def __init__(self, _id, sensor_list, rule_list):
    self.sensor_list = sensor_list
    self.rule_list = rule_list
    self._id = _id
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})

  def get_device_id(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["device_id"]

  def get_sensor_name(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["sensor_name"]

  def get_sensor_id(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["sensor_id"]

  def get_time_added(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["time_added"]

  def get_last_data_added_time(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["last_data_added_time"]

  def get_total_data_entry(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["total_data_entry"]

  def get_api_key(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["api_key"]

  def get_total_rule(self):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return self.sensor_document["total_rule"]

  def change_sensor_info(self, **sensor_info):
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    for key, value in sensor_info.iteritems():
      self.sensor_document[key] = value
    self.sensor_list.save(self.sensor_document)
    return True

  def post_data(self, data_value):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data_entry = {"time_added":date[:-7],"_time_added":date,"data_value":data_value}
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    self.sensor_document["data_collection"].append(data_entry)
    self.sensor_document["last_data_added_time"] = date[:-7]
    self.sensor_document["total_data_entry"] += 1
    self.sensor_list.save(self.sensor_document)
    return True

  def get_data(self, get_from=0, to=-1):
    time_added_list = sorted([x["_time_added"] for x in sensor.sensor_document["data_collection"]],reverse=True)
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})
    return [x for x in sensor.sensor_document["data_collection"] if x["_time_added"] in time_added_list]

  def get_rule_list(self):
    rule_list = [Rule(x["_id"],self.rule_list) for x in self.rule_list.find({"api_key":self.get_api_key(),"device_id":self.get_device_id(),"sensor_id":self.get_sensor_id()})]
    return rule_list

  def find_rule(self, rule_id):
    rule_info = self.rule_list.find_one({"sensor_id":self.get_sensor_id(),"api_key":self.get_api_key(),"rule_id":rule_id})
    if rule_info:
      _id = rule_info["_id"]
      return Rule(_id, self.rule_list)
    else:
      return False

  def add_rule(self, rule_id, rule_name, expected_value, operator, value, endpoint, command):
    if not self.find_rule(rule_id) and expected_value in ['INT','STR'] and operator in ['EQU','NEQ','LSS','LEQ','GTR','GEQ']:
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      mongo_id = self.rule_list.insert_one({
          "api_key":self.get_api_key(),
          "device_id":self.get_device_id(),
          "sensor_id":self.get_sensor_id(),
          "rule_id":rule_id,
          "rule_name":rule_name,
          "expected_value":expected_value,
          "operator":operator,
          "value":value,
          "endpoint":endpoint,
          "command":command,
          "time_added":date
        })
      _id = mongo_id.inserted_id
      self.sensor_document = self.sensor_list.find_one({"_id":self._id})
      self.sensor_document["total_rule"] += 1
      self.sensor_list.save(self.sensor_document)
      return Rule(_id, self.rule_list)
    else:
      return False

  def remove_rule(self, rule_id):
    rule_info = self.find_rule(rule_id)
    if rule_info:
      self.rule_list.remove({"_id":rule_info._id})
      self.sensor_document = self.sensor_list.find_one({"_id":self._id})
      self.sensor_document["total_rule"] -= 1
      self.sensor_list.save(self.sensor_document)
      return True
    else:
      return False

class Rule(Sensor):
  def __init__(self, _id, rule_list):
    self.rule_list = rule_list
    self._id = _id
    self.rule_document = self.rule_list.find_one({"_id":self._id})

  def get_api_key(self):
      self.rule_document = self.rule_list.find_one({"_id":self._id})
      return self.rule_document["api_key"]

  def get_device_id(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["device_id"]

  def get_sensor_id(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["sensor_id"]

  def get_rule_name(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["rule_name"]

  def get_rule_id(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["rule_id"]

  def get_time_added(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["time_added"]

  def get_expected_value(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["expected_value"]

  def get_operator(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["operator"]

  def get_value(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["value"]

  def get_endpoint(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["endpoint"]

  def get_command(self):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    return self.rule_document["command"]

  def change_rule_info(self, **rule_info):
    self.rule_document = self.rule_list.find_one({"_id":self._id})
    for key, value in rule_info.iteritems():
      self.rule_document[key] = value
    self.rule_list.save(self.rule_document)
    return True

  def compare (self, data):
    try:
      if self.get_operator() == "EQU":
        if data == self.get_value():
          return True
        else:
          return False
      elif self.get_operator() == "NEQ":
        if data != self.get_value():
          return True
        else:
          return False
      elif self.get_operator() == "LSS":
        if data < self.get_value():
          return True
        else:
          return False
      elif self.get_operator() == "LEQ":
        if data <= self.get_value():
          return True
        else:
          return False
      elif self.get_operator() == "GTR":
        if data > self.get_value():
          return True
        else:
          return False
      elif self.get_operator() == "GEQ":
        if data >= self.get_value():
          return True
        else:
          return False
      else:
        return False
    except:
      return False