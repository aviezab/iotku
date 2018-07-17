# iotku  
An open source IoT Platform made from Python and MongoDB. Designed for medium scale. Made by Indonesia.  
https://iotku.id  
https://dev.iotku.id  

iotKu - Sebuah Platform IOT Terbuka dari Indonesia  
==================================================  
Proyek ini diinisiasi oleh komunitas IT Indonesia  
Februari 2018  
iotKu menggunakan 2 script python untuk berfungsi, jadi siapkan 2 shell  
(atau jadikan service)  

Cara memakai:  
- Install dan setting MongoDB, Redis, dan NATS sesuai kebutuhan  
- cd iotku  
- python3 app.py  
- python3 subscribe.py  

Cara Pakai API iotKu
==================================================  
List API, Register dan Login -- https://iotku.id/IoTKu_Register_Login.html
API lengkap -- https://iotku.id/IoTKu_API.html

Dependency and Supporting Engine  
==================================================  
Flask  
Asyncio-NATS  
py-Redis  
py-Mongo  
for complete dependencies, see requirements.txt at iotku folder.  

MongoDB https://www.mongodb.com  
Redis Memory Cache https://redis.io  
NATS Message Broker https://nats.io  

Dockerized version: https://github.com/icarus213/iotkudocker

(C) 2018 iotKu Team. Indonesia.  
Initiated by aviezab  
