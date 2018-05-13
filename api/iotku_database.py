# iotKu Database Model
# 
# iotKu - User
#       \
#         User - Device
#              \
#                Device - Sensor
#                       \
#                         Sensor -- Rule
#                                |\
#                                |  Rule
#                                 \
#                                   Rule

# Dibutuhkan untuk connect ke MongoDB
from pymongo import MongoClient

# Dibutuhkan untuk menghasilkan API key, yaitu MD5 hash dari email
import hashlib

# Dibutuhkan untuk mendapatkan tanggal dan waktu saat berbagai operasi berlangsung
import datetime

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

    # -----------------------------------------------------------------------------------
    # Fungsi:
    # - untuk inisialisasi variabel-variable penting
    # Penjelasan:
    # - db adalah nama database (tipe string)
    # - user_list adalah nama collection untuk document-document user (tipe string)
    # - device_list adalah nama collection untuk document-document device (tipe string)
    # - sensor_list adalah nama collection untuk document-document sensor (tipe string)
    # - rule_list adalah nama collection untuk document-document rule (tipe string)
    # -----------------------------------------------------------------------------------

    # Cek tipe variabel-variable
    assert type(db) == type(str())
    assert type(user_list) == type(str())
    assert type(device_list) == type(str())
    assert type(sensor_list) == type(str())
    assert type(rule_list) == type(str())

    # Init client
    self.client = client

    # Init database
    self.db = self.client[db]

    # Init user_list collection
    self.user_list = self.db[user_list]

    # Init device_list collection
    self.device_list = self.db[device_list]

    # Init sensor_list collection
    self.sensor_list = self.db[sensor_list]

    # Init rule_list collection
    self.rule_list = self.db[rule_list]



  def get_user_list(self):
    # -----------------------------------------------
    # Fungsi:
    # - untuk mendapatkan list user di database iotKu
    # Penjelasan:
    # - function ini tidak memerlukan parameter
    # -----------------------------------------------

    # List untuk instance user-user
    user_list = []

    # Berisi document user-user
    user_docs = list(self.user_list.find({}))

    # Iteration 1
    for x in user_docs:
      # Mendapatkan id dari document x (id digenerate otomatis oleh MongoDB)
      _id = x['_id']

      # Menghasilkan instance User dengan id dari document
      user = User(_id, self.user_list, self.device_list, self.sensor_list, self.rule_list)

      # Menambahkan instance user kedalam user_list
      user_list.append(user)

    # Iteration 1 selesai

    # Return user_list
    return user_list



  def find_user(self, **user_info):
    # --------------------------------------------------------------------------------
    # Fungsi:
    # - untuk mencari dan mendapatkan user
    # Penjelasan:
    # - user_info bertipe dictionary yang berisi info-info yang akan digunakan untuk 
    #   mencari user, misalnya email
    #   Catatan: walaupun user_info bertipe dictionary, namun parameter yang digunakan
    #            bukanlah variable dictionary dengan nama user_info
    #            (search 'python kwargs')
    # --------------------------------------------------------------------------------

    # Mencari document user di database berdasarkan user_info
    result = self.user_list.find_one(user_info)

    # Jika tidak ketemu:
    if not result:
      # Return false
      return False

    # Jika ketemu:
    else:
      # Mendapatkan id dari document result
      _id = result["_id"]

      # Menghasilkan instance User dengan id dari document
      user = User(_id, self.user_list, self.device_list, self.sensor_list, self.rule_list)
      
      # Return user
      return user

  def add_user(self, email, password):
    # ---------------------------------------------------------------------
    # Fungsi:
    # - untuk menambahkan user ke database
    # Penjelasan:
    # - email bertipe string berisi email user yang akan ditambahkan
    # - password bertipe string berisi password user yang akan ditambahkan
    # ---------------------------------------------------------------------

    # Jika user dengan email sama terdapat di database:
    if self.find_user(email=email):
      # Return false
      return False

    # Jika user dengan email sama tidak terdapat di database:
    else:
      # Mendapatkan tanggal dan waktu saat function dipanggil
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # Membuat struktur document user
      doc = {
              # Entri: 
              # - email berisi email
              # - password berisi password
              # - api_key berisi md5 hash email
              # - time_added berisi date
              # - total_device berisi banyak device yang user punya
              'email': email,
              'password': password,
              'api_key': hashlib.md5(email.encode('ascii')).hexdigest(),
              'time_added': date,
              'total_device': 0
            }

      # Memasukkan document ke database
      inserted = self.user_list.insert_one(doc)

      # Mendapatkan id dari document yang baru saja dimasukkan
      _id = inserted.inserted_id

      # Menghasilkan instance User dengan id dari document
      user = User(_id, self.user_list, self.device_list, self.sensor_list, self.rule_list)
      
      # Return user
      return user

  def remove_user(self, email):
    # -------------------------------------------------------------
    # Fungsi:
    # - untuk menghapus user
    # Penjelasan:
    # - email adalah email user yang ingin dihapus (bertipe string)
    # -------------------------------------------------------------

    # Mencari user dengan email yang sama
    user_info = self.find_user(email = email)

    # Jika tidak ketemu:
    if not user_info:
      # Return false
      return False

    # Jika ketemu
    else:
      # Menghapus user dari database
      self.user_list.remove({"_id":user_info._id})

      # Menghapus device-device user dari database
      self.device_list.remove({"api_key":user_info.get('api_key')})

      # Menghapus sensor-sensor user dari database
      self.sensor_list.remove({"api_key":user_info.get('api_key')})

      # Menghapus rule-rule user dari database
      self.rule_list.remove({"api_key":user_info.get('api_key')})

      # Return true
      return True

class User(Iotku):
  def __init__(self, _id, user_list, device_list, sensor_list, rule_list):
    # -----------------------------------------------------------------------------------
    # Fungsi:
    # - untuk inisialisasi variabel-variable penting
    # Penjelasan:
    # - _id adalah id document user
    # - user_list adalah nama collection untuk document-document user (tipe string)
    # - device_list adalah nama collection untuk document-document device (tipe string)
    # - sensor_list adalah nama collection untuk document-document sensor (tipe string)
    # - rule_list adalah nama collection untuk document-document rule (tipe string)
    # -----------------------------------------------------------------------------------

    # Init variable user_list
    self.user_list = user_list

    # Init variable device_list
    self.device_list = device_list

    # Init variable sensor_list
    self.sensor_list = sensor_list

    # Init variable rule_list
    self.rule_list = rule_list

    # Init variable _id
    self._id = _id

  def change_user_info(self, email = None,password = None):
    # ------------------------------------------
    # Fungsi:
    # - untuk mengganti info device
    # Penjelasan:
    # - email bertipe string, nilai default None
    # - password bertipe string, nilai default None
    # ------------------------------------------

    # Mendapatkan document user berdasarkan variable _id
    user_document = self.user_list.find_one({"_id":self._id})

    # Jika user tidak terdapat di DB
    if not user_document:
      # Return false
      return False

    # Jika user terdapat di DB
    else:
      # Jika nilai email bukan None:
      if email != None:
        # Mengganti email user
        user_document['email'] = email

        # Mengganti api_key user
        user_document['api_key'] = hashlib.md5(email.encode('ascii')).hexdigest()

      # Jika nilai password bukan None:
      if password != None:
        # Mengganti password user
        user_document['password'] = password

      # Save document
      self.user_list.save(user_document)

      # Return True
      return True

  def get(self, key):
    # --------------------------------------------------------
    # Fungsi:
    # - mendapatkan info user
    # Penjelasan:
    # - key bertipe string, untuk mendapatkan apa yang diminta
    #   (contoh: key = "email" untuk mendapatkan email user)
    # --------------------------------------------------------

    # Mendapatkan document user
    self.user_document = self.user_list.find_one({"_id":self._id})

    # Return value (jika tidak ada, akan return None)
    return self.user_document.get(key)

  def get_device_list(self):
    # ----------------------------------------------
    # Fungsi:
    # - mendapatkan device-device yang dipunyai user
    # Penjelasan:
    # - fungsi ini tidak memerlukan parameter
    # ----------------------------------------------

    # List untuk instance device-device
    device_list = []

    # Berisi document device-device
    device_docs = list(self.device_list.find({"api_key": self.get('api_key')}))

    # Iteration 1
    for x in device_docs:
      # Mendapatkan id dari document x (id digenerate otomatis oleh MongoDB)
      _id = x['_id']

      # Menghasilkan instance Device dengan id dari document
      device = Device(_id, self.device_list, self.sensor_list, self.rule_list)

      # Menambahkan instance device ke dalam device_list
      device_list.append(device)

    # Iteration 1 selesai

    # Return device_list
    return device_list


  def find_device(self, device_id):
    # -----------------------------------------
    # Fungsi:
    # - mencari dan mendapatkan instance device
    # Penjelasan:
    # - device_id bertipe string
    # -----------------------------------------

    # Mendapatkan document device
    device_info = self.device_list.find_one({"device_id":device_id,"api_key":self.get('api_key')})

    # Jika tidak ketemu
    if not device_info:
      # Return false
      return False
    else:
      # Id document
      _id = device_info["_id"]

      # Return instance device
      return Device(_id, self.device_list, self.sensor_list, self.rule_list)

  def add_device(self, device_id, device_name):
    # ----------------------------
    # Fungsi:
    # - menambah device
    # Penjelasan:
    # - device_id bertipe string
    # - device_name bertipe string
    # ----------------------------

    # Jika device dengan id yang sama terdapat di database:
    if self.find_device(device_id):
      # Return false
      return False
    # Jika tidak:
    else:
      # Mendapatkan tanggal dan waktu
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # Memasukkan device ke database
      mongo_id = self.device_list.insert_one({
                      "api_key":self.get('api_key'),
                      "device_id":device_id,
                      "device_name":device_name,
                      "total_sensor":0,
                      "time_added":date,
                      "command": dict(),
                      "command_history": []
                      })

      # Mendapatkan document user
      self.user_document = self.user_list.find_one({"_id":self._id})

      # Menambahkan total_device
      self.user_document["total_device"] += 1

      # Save document user
      self.user_list.save(self.user_document)

      # Id document
      _id = mongo_id.inserted_id

      # Return instance device
      return Device(_id, self.device_list, self.sensor_list, self.rule_list)

  def remove_device(self, device_id):
    # --------------------------
    # Fungsi:
    # - menghapus device
    # Penjelasan:
    # - device_id bertipe string
    # --------------------------

    # Mencari device dengan id sama
    device_info = self.find_device(device_id)

    # Jika tidak ketemu
    if not device_info:
      # Return false
      return False
    # Jika ketemu
    else:
      # Menghapus device dari database
      self.device_list.remove({"_id":device_info._id})

      # Mendapatkan document user
      self.user_document = self.user_list.find_one({"_id":self._id})

      # Mengurangi total_device
      self.user_document["total_device"] -= 1

      # Save document user
      self.user_list.save(self.user_document)

      # Menghapus sensor-sensor device
      self.sensor_list.remove({"api_key":self.get('api_key'),"device_id":device_id})

      # Menghapus rule-rule sensor device
      self.rule_list.remove({"api_key":self.get('api_key'),"device_id":device_id})

      # Return True
      return True

class Device(User):
  def __init__(self, _id, device_list, sensor_list, rule_list):
    # -----------------------------------------------------------------------------------
    # Fungsi:
    # - untuk inisialisasi variabel-variable penting
    # Penjelasan:
    # - _id adalah id document device
    # - device_list adalah nama collection untuk document-document device (tipe string)
    # - sensor_list adalah nama collection untuk document-document sensor (tipe string)
    # - rule_list adalah nama collection untuk document-document rule (tipe string)
    # -----------------------------------------------------------------------------------

    # Init variable device_list
    self.device_list = device_list

    # Init variable sensor_list
    self.sensor_list = sensor_list

    # Init variable rule_list
    self.rule_list = rule_list

    # Init variable _id
    self._id = _id

  def get(self, key):
    # --------------------------------------------------------
    # Fungsi:
    # - mendapatkan info device
    # Penjelasan:
    # - key bertipe string, untuk mendapatkan apa yang diminta
    #   (contoh: key = "device_id" untuk mendapatkan id device)
    # --------------------------------------------------------

    # Mendapatkan document device
    self.device_document = self.device_list.find_one({"_id":self._id})

    # Return value (jika tidak ada, akan return None)
    return self.device_document.get(key)

  def change_device_info(self, device_id = None, device_name = None):
    # ------------------------------------------
    # Fungsi:
    # - untuk mengganti info user
    # Penjelasan:
    # - device_id bertipe string, nilai default None
    # - device_name bertipe string, nilai default None
    # ------------------------------------------

    # Mendapatkan document device berdasarkan variable instance _id
    device_document = self.device_list.find_one({"_id":self._id})

    # Jika device tidak terdapat di DB
    if not device_document:
      # Return false
      return False

    # Jika device terdapat di DB
    else:
      # Jika nilai device_id bukan None:
      if device_id != None:

        # Iteration 1
        for x in self.sensor_list.find({'api_key': self.get('api_key'), 'device_id': self.get('device_id')}):
          # Mengganti id device sensor
          x['device_id'] = device_id
        # Iteration 1 selesai

        # Iteration 2
        for x in self.rule_list.find({'api_key': self.get('api_key'), 'device_id': self.get('device_id')}):
          # Mengganti id device rule
          x['device_id'] = device_id
        # Iteration 2 selesai

        # Mengganti id device
        device_document['device_id'] = device_id

      # Jika nilai device_name bukan None:
      if device_name != None:
        # Mengganti nama device
        device_document['device_name'] = device_name

      # Save document
      self.device_list.save(device_document)

      # Return True
      return True

  def get_sensor_list(self):
    # ----------------------------------------------
    # Fungsi:
    # - mendapatkan sensor-sensor yang dipunyai device
    # Penjelasan:
    # - fungsi ini tidak memerlukan parameter
    # ----------------------------------------------

    # List untuk instance sensor-sensor
    sensor_list = []

    # Berisi document sensor-sensor
    sensor_docs = list(self.sensor_list.find({"api_key": self.get('api_key'),"device_id": self.get('device_id')}))

    # Iteration 1
    for x in sensor_docs:
      # Mendapatkan id dari document x (id digenerate otomatis oleh MongoDB)
      _id = x['_id']

      # Menghasilkan instance Sensor dengan id dari document
      sensor = Sensor(_id, self.sensor_list, self.rule_list)

      # Menambahkan instance sensor ke dalam sensor_list
      sensor_list.append(sensor)

    # Iteration 1 selesai

    # Return sensor_list
    return sensor_list

  def find_sensor(self, sensor_id):
    # -----------------------------------------
    # Fungsi:
    # - mencari dan mendapatkan instance sensor
    # Penjelasan:
    # - sensor_id bertipe string
    # -----------------------------------------

    # Mendapatkan document sensor
    sensor_info = self.sensor_list.find_one({"sensor_id":sensor_id, "device_id": self.get('device_id'), "api_key":self.get('api_key')})

    # Jika tidak ketemu
    if not sensor_info:
      # Return false
      return False
    else:
      # Id document
      _id = sensor_info["_id"]

      # Return instance Sensor
      return Sensor(_id, self.sensor_list, self.rule_list)

  def add_sensor(self, sensor_id, sensor_name):
    # ----------------------------
    # Fungsi:
    # - menambah sensor
    # Penjelasan:
    # - sensor_id bertipe string
    # - sensor_name bertipe string
    # ----------------------------

    # Jika sensor dengan id yang sama terdapat di database:
    if self.find_sensor(sensor_id):
      # Return false
      return False
    # Jika tidak:
    else:
      # Mendapatkan tanggal dan waktu
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # Memasukkan sensor ke database
      mongo_id = self.sensor_list.insert_one({
          "api_key":self.get("api_key"),
          "device_id":self.get("device_id"),
          "sensor_id":sensor_id,
          "sensor_name":sensor_name,
          "last_data_added_time":"Never",
          "total_data_entry":0,
          "total_rule":0,
          "data_collection":[],
          "time_added":date
        })

      # Mendapatkan document device
      self.device_document = self.device_list.find_one({"_id":self._id})

      # Menambahkan total_sensor
      self.device_document["total_sensor"] += 1

      # Save document device
      self.device_list.save(self.device_document)

      # Id document
      _id = mongo_id.inserted_id

      # Return instance sensor
      return Sensor(_id, self.sensor_list, self.rule_list)

  def remove_sensor(self, sensor_id):
    # --------------------------
    # Fungsi:
    # - menghapus sensor
    # Penjelasan:
    # - sensor_id bertipe string
    # --------------------------

    # Mencari sensor dengan id sama
    sensor_info = self.find_sensor(sensor_id)

    # Jika tidak ketemu
    if not sensor_info:
      # Return false
      return False
    # Jika ketemu
    else:
      # Menghapus sensor dari database
      self.sensor_list.remove({"_id":sensor_info._id})

      # Mendapatkan document device
      self.device_document = self.device_list.find_one({"_id":self._id})

      # Mengurangi total_sensor
      self.device_document["total_sensor"] -= 1

      # Save document device
      self.device_list.save(self.device_document)

      # Menghapus rule-rule sensor
      self.rule_list.remove({"api_key":self.get('api_key'),"device_id":self.get("device_id"),"sensor_id": sensor_id})

      # Return True
      return True

  def send_command(self, command):
    # -------------------------------------------------------------------------------
    # Fungsi:
    # - mengganti command di database
    # Penjelasan:
    # - command bertipe string, adalah command yang akan mengganti command sebelumnya
    # -------------------------------------------------------------------------------

    # Mendapatkan tanggal dan waktu
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Membuat struktur dictionary
    data_entry = {"time_added":date[:-7],"_time_added":date,"command":command}

    # Mendapatkan document device
    self.device_document = self.device_list.find_one({"_id":self._id})

    # Menambahkan data_entry ke command_history
    self.device_document["command_history"].append(data_entry)

    # Mengganti command menjadi data_entry
    self.device_document["command"] = data_entry

    # Save document
    self.device_list.save(self.device_document)

    # Return true
    return True

class Sensor(Device):
  def __init__(self, _id, sensor_list, rule_list):
    # -----------------------------------------------------------------------------------
    # Fungsi:
    # - untuk inisialisasi variabel-variable penting
    # Penjelasan:
    # - _id adalah id document device
    # - sensor_list adalah nama collection untuk document-document sensor (tipe string)
    # - rule_list adalah nama collection untuk document-document rule (tipe string)
    # -----------------------------------------------------------------------------------

    # Init variable sensor_list
    self.sensor_list = sensor_list

    # Init variable rule_list
    self.rule_list = rule_list

    # Init variable _id
    self._id = _id

  def get(self, key):
    # --------------------------------------------------------
    # Fungsi:
    # - mendapatkan info sensor
    # Penjelasan:
    # - key bertipe string, untuk mendapatkan apa yang diminta
    #   (contoh: key = "sensor_id" untuk mendapatkan id sensor)
    # --------------------------------------------------------

    # Mendapatkan document sensor
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})

    # Return value (jika tidak ada, akan return None)
    return self.sensor_document.get(key)

  def change_sensor_info(self, sensor_id = None, sensor_name = None):
    # ------------------------------------------
    # Fungsi:
    # - untuk mengganti info sensor
    # Penjelasan:
    # - sensor_id bertipe string, nilai default None
    # - sensor_name bertipe string, nilai default None
    # ------------------------------------------

    # Mendapatkan document sensor berdasarkan variable instance _id
    sensor_document = self.sensor_list.find_one({"_id":self._id})

    # Jika sensor tidak terdapat di DB
    if not sensor_document:
      # Return false
      return False

    # Jika sensor terdapat di DB
    else:
      # Jika nilai sensor_id bukan None:
      if sensor_id != None:

        # Iteration 1
        for x in self.rule_list.find({'api_key': self.get('api_key'), 'device_id': self.get('device_id'), 'sensor_id': self.get('sensor_id')}):
          # Mengganti id sensor rule
          x['sensor_id'] = sensor_id
        # Iteration 1 selesai

        # Mengganti id sensor
        sensor_document['sensor_id'] = sensor_id

      # Jika nilai sensor_name bukan None:
      if sensor_name != None:
        # Mengganti nama sensor
        sensor_document['sensor_name'] = sensor_name

      # Save document
      self.sensor_list.save(sensor_document)

      # Return True
      return True

  def post_data(self, data_value):
    # ------------------------------------
    # Fungsi:
    # - memasukkan data sensor ke database
    # Penjelasan
    # - data_value bebas bertipe apa saja
    # ------------------------------------

    # Mendapatkan tanggal dan waktu
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Membuat struktur dictionary
    data_entry = {"time_added":date[:-7],"_time_added":date,"data_value":data_value}

    # Mendapatkan document sensor
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})

    # Memasukkan data_entry ke list data-data sensor
    self.sensor_document["data_collection"].append(data_entry)

    # Mengganti last_data_added_time
    self.sensor_document["last_data_added_time"] = date[:-7]

    # Menambahkan total_data_entry
    self.sensor_document["total_data_entry"] += 1

    # Save document
    self.sensor_list.save(self.sensor_document)

    # Return ture
    return True

  def get_data(self, get_from=0, to=-1):
    # ------------------------------------------
    # Fungsi:
    # - Mendapatkan data sensor
    # Penjelasan:
    # - get_from bertipe int, sebagai index awal
    # - to bertipe int, sebagai index akhir
    # ------------------------------------------

    # Sorting data_entry menurut waktu dari yang terbaru sampai yang terlama
    time_added_list = sorted([x["_time_added"] for x in sensor.sensor_document["data_collection"]],reverse=True)[get_from:to]

    # Mendapatkan document sensor
    self.sensor_document = self.sensor_list.find_one({"_id":self._id})

    # Return data_entry
    return [x for x in sensor.sensor_document["data_collection"] if x["_time_added"] in time_added_list]

  def get_rule_list(self):
    # ----------------------------------------------
    # Fungsi:
    # - mendapatkan rule-rule yang dipunyai sensor
    # Penjelasan:
    # - fungsi ini tidak memerlukan parameter
    # ----------------------------------------------

    # List untuk instance rule-rule
    rule_list = []

    # Berisi document rule-rule
    rule_docs = list(self.rule_list.find({"api_key": self.get('api_key'),"device_id": self.get('device_id'),"sensor_id": self.get('sensor_id')}))

    # Iteration 1
    for x in rule_docs:
      # Mendapatkan id dari document x (id digenerate otomatis oleh MongoDB)
      _id = x['_id']

      # Menghasilkan instance rule dengan id dari document
      rule = Rule(_id, self.rule_list)

      # Menambahkan instance rule ke dalam rule_list
      rule_list.append(rule)

    # Iteration 1 selesai

    # Return rule_list
    return rule_list

  def find_rule(self, rule_id):
    # -----------------------------------------
    # Fungsi:
    # - mencari dan mendapatkan instance rule
    # Penjelasan:
    # - rule_id bertipe string
    # -----------------------------------------

    # Mendapatkan document rule
    rule_info = self.rule_list.find_one({"rule_id": rule_id, "sensor_id":self.get('sensor_id'), "device_id": self.get('device_id'), "api_key":self.get('api_key')})

    # Jika tidak ketemu
    if not rule_info:
      # Return false
      return False
    else:
      # Id document
      _id = rule_info["_id"]

      # Return instance Rule
      return Rule(_id, self.rule_list)

  def add_rule(self, rule_id, rule_name, expected_type, condition, endpoint, command):
    # ---------------------------------
    # Fungsi:
    # - menambah rule
    # Penjelasan:
    # - rule_id bertipe string
    # - rule_name bertipe string
    # - condition bertipe list, berisi
    # -- operator, bertipe string
    # -- value, bertipe string atau int
    # - endpoint bertipe string
    # - command bertipe string
    # ---------------------------------

    # Jika rule dengan id yang sama terdapat di database:
    if self.find_rule(rule_id):
      # Return false
      return False
    # Jika tidak:
    else:
      # Mendapatkan tanggal dan waktu
      date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # Memasukkan rule ke database
      mongo_id = self.rule_list.insert_one({
          "api_key":self.get('api_key'),
          "device_id":self.get('device_id'),
          "sensor_id":self.get('sensor_id'),
          "rule_id":rule_id,
          "rule_name":rule_name,
          "expected_type":expected_type,
          "condition":condition,
          "endpoint":endpoint,
          "command":command,
          "time_added":date
        })

      # Mendapatkan document sensor
      self.sensor_document = self.sensor_list.find_one({"_id":self._id})

      # Menambahkan total_rule
      self.sensor_document["total_rule"] += 1

      # Save document sensor
      self.sensor_list.save(self.sensor_document)

      # Id document
      _id = mongo_id.inserted_id

      # Return instance Rule
      return Rule(_id, self.rule_list)

  def remove_rule(self, rule_id):
    # ------------------------
    # Fungsi:
    # - menghapus rule
    # Penjelasan:
    # - rule_id bertipe string
    # ------------------------

    # Mencari rule dengan id sama
    rule_info = self.find_rule(rule_id)

    # Jika tidak ketemu
    if not rule_info:
      # Return false
      return False
    # Jika ketemu
    else:
      # Menghapus rule dari database
      self.rule_list.remove({"_id":rule_info._id})

      # Mendapatkan document sensor
      self.sensor_document = self.sensor_list.find_one({"_id":self._id})

      # Mengurangi total_rule
      self.sensor_document["total_rule"] -= 1

      # Save document sensor
      self.sensor_list.save(self.sensor_document)

      # Return True
      return True

class Rule(Sensor):
  def __init__(self, _id, rule_list):
    # -----------------------------------------------------------------------------------
    # Fungsi:
    # - untuk inisialisasi variabel-variable penting
    # Penjelasan:
    # - _id adalah id document device
    # - rule_list adalah nama collection untuk document-document rule (tipe string)
    # -----------------------------------------------------------------------------------

    # Init variable rule_list
    self.rule_list = rule_list

    # Init variable _id
    self._id = _id

  def get(self, key):
    # --------------------------------------------------------
    # Fungsi:
    # - mendapatkan info rule
    # Penjelasan:
    # - key bertipe string, untuk mendapatkan apa yang diminta
    #   (contoh: key = "rule_id" untuk mendapatkan id rule)
    # --------------------------------------------------------

    # Mendapatkan document rule
    self.rule_document = self.rule_list.find_one({"_id":self._id})

    # Return value (jika tidak ada, akan return None)
    return self.rule_document.get(key)

  def change_rule_info(self, rule_id = None, rule_name = None, expected_type = None, 
                          condition = None, endpoint = None, command = None):
    # ------------------------------------------
    # Fungsi:
    # - untuk mengganti info rule
    # Penjelasan:
    # - rule_id bertipe string, nilai default None
    # - rule_name bertipe string, nilai default None
    # ------------------------------------------

    # Mendapatkan document sensor berdasarkan variable instance _id
    rule_document = self.rule_list.find_one({"_id":self._id})

    # Jika rule tidak terdapat di DB
    if not rule_document:
      # Return false
      return False

    # Jika rule terdapat di DB
    else:
      # Jika nilai rule_id bukan None:
      if rule_id != None:
        # Mengganti id rule
        rule_document['rule_id'] = rule_id

      # Jika nilai rule_name bukan None:
      if rule_name != None:
        # Mengganti nama rule
        rule_document['rule_name'] = rule_name

      if expected_type != None:
        # Mengganti expected_type rule
        rule_document['expected_type'] = expected_type

      if condition != None:
        # Mengganti condition rule
        rule_document['condition'] = condition

      if endpoint != None:
        # Mengganti endpoint rule
        rule_document['endpoint'] = endpoint

      if command != None:
        # Mengganti command rule
        rule_document['command'] = command

      # Save document
      self.rule_list.save(rule_document)

      # Return True
      return True

  def compare (self, data):
    # -------------------------------------------------------
    # Fungsi:
    # - logic
    # Penjelasan:
    # - data boleh bertipe apa saja, akan dikonversi otomatis
    # -------------------------------------------------------
    try:
      if self.get('expected_type').upper() == 'STR':
        data = str(data)
      elif self.get('expected_type').upper() == 'INT':
        data = int(data)
      for x in self.get('condition'):
        if x.get('operator') == "EQU":
          if data == x.get('value'):
            continue
          else:
            return False
        elif x.get('operator') == "NEQ":
          if data != x.get('value'):
            continue
          else:
            return False
        elif x.get('operator') == "LSS":
          if data < x.get('value'):
            continue
          else:
            return False
        elif x.get('operator') == "LEQ":
          if data <= x.get('value'):
            continue
          else:
            return False
        elif x.get('operator') == "GTR":
          if data > x.get('value'):
            continue
          else:
            return False
        elif x.get('operator') == "GEQ":
          if data >= x.get('value'):
            continue
          else:
            return False
        else:
          return False
    except:
      return False
    return True