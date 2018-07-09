from api import iotku, c
import datetime
import asyncio

class iotku_custom_handler:
    @asyncio.coroutine
    def post_handler(self, msg):
        # DEBUG: print('ENTERING post_handler')
        print("[Received on '{}']: {}".format(msg.subject, msg.data.decode()))
        api_key = bytes.fromhex(msg.data.decode().split(' , ')[0]).decode('ascii')
        device_id = bytes.fromhex(msg.data.decode().split(' , ')[1]).decode('ascii')
        sensor_id = bytes.fromhex(msg.data.decode().split(' , ')[2]).decode('ascii')
        data = bytes.fromhex(msg.data.decode().split(' , ')[3]).decode('ascii')
        user = iotku.find_user(api_key=api_key)
        device = user.find_device(device_id)
        sensor = device.find_sensor(sensor_id)
        sensor.post_data(data)
        rule_list = sensor.get_rule_list()
        for x in rule_list:
            if x.compare(data):
                device = user.find_device(x.get('endpoint'))
                if device:
                    device.send_command(x.get('command'))

        # DEBUG: print('EXITING post_handler')

c.subscribe(subject="post",queue="worker",cb=iotku_custom_handler.post_handler)
print('READY')
c.start_loop()
