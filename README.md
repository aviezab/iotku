# iotku
An open source IoT Platform made from Python and MongoDB. Designed for medium scale. Made by Indonesia.
https://iotku.id
https://dev.iotku.id

iotKu - Sebuah Platform IOT Terbuka dari Indonesia
==================================================
Proyek ini diinisiasi oleh komunitas IT Indonesia
Pebruari 2018

Untuk Windows
Jalankan redis-server.exe
Jalankan Mongodb - "C:\Program Files\MongoDB\Server\3.6\bin\mongod.exe" --dbpath=db

Untuk Linux
cd iotkusite
cek redis jalan atau tidak: redis-cli
ketik ping, apabila dibalas pong berarti redis sudah jalan.
mongod --dbpath=db
python3 web.py


Dependency and Supporting Engine
==================================================
Flask
Asyncio-NATS
py-Redis
py-Mongo
for completed dependencies, see Requirements.txt at iotkusite folder.

Redis Memory Cache redis https://redis.io
NATS Message Broker https://nats.io

(C) 2018 iotKu Team. Indonesia.
Initiated by aviezab
