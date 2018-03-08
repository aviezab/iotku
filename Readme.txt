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