import asyncio
import os
import signal
from nats.aio.client import Client as NATS

class NATS:
    def __init__(self, nc=NATS(), loop=asyncio.get_event_loop()):
        self.nc = nc
        self.loop = loop

        # List topic topic yang disubscribe
        self.sub_list = []

        # Option untuk connect ke NATS server
        self.options = {"servers": ["nats://127.0.0.1:4222"],"io_loop": self.loop}

        self.sid = []

        self.pub_stay_connected = True

    def __del__(self):
        try:
            self.loop.run_until_complete(self.close())
        except:
            pass
        self.loop.stop()

    # SUBSCRIBE FEATURE
    @asyncio.coroutine
    def message_handler(self, msg):
        print("[Received on '{}']: {}".format(msg.subject, msg.data.decode()))

    @asyncio.coroutine
    def closed_cb(self):
        print("Connection to NATS is closed.")
        yield from asyncio.sleep(0.1, loop=self.loop)
        self.loop.stop()

    # syntax sama dengan syntax subscribe asyncio-nats
    def subscribe(self, subject, queue="", cb=message_handler, future=None, max_msgs=0, is_async=False):
        cb = cb.__get__(self, NATS)
        self.sub_list.append({'subject': subject,'queue': queue,'cb': cb,'future': future,'max_msgs': max_msgs,'is_async': is_async})

    @asyncio.coroutine
    def _start(self):
        if "closed_cb" not in self.options:
            self.options['closed_cb'] = self.closed_cb
        try:
            yield from self.nc.connect(**self.options)
        except:
            pass
        nc = self.nc
        for x in self.sub_list:
            yield from nc.subscribe(**x)
        def signal_handler():
            if nc.is_closed:
                return
            print("Disconnecting...")
            self.loop.create_task(nc.close())
        for sig in ('SIGINT', 'SIGTERM'):
            self.loop.add_signal_handler(getattr(signal, sig), signal_handler)

    def start_loop(self):
        self.loop.run_until_complete(self._start())
        try:
          self.loop.run_forever()
        finally:
          self.loop.close()
    # END SUBSCRIBE FEATURE

    # PUBLISH FEATURE

    @asyncio.coroutine
    def connect(self):
        yield from self.nc.connect(**self.options)

    @asyncio.coroutine
    def close(self):
        yield from self.nc.close()

    def publish(self, subject, payload):
        if not self.nc.is_connected:
            # DEBUG: print('not connected')
            self.loop.run_until_complete(self.connect())
        self.loop.run_until_complete(self.nc.publish(subject,payload))
        if not self.pub_stay_connected:
            self.close()
        return

    def timed_request(self, subject, payload, timeout=0.5):
        if not self.nc.is_connected:
            # DEBUG: print('not connected')
            self.loop.run_until_complete(self.connect())
        ret = self.loop.run_until_complete(self.nc.timed_request(subject,payload,timeout))
        if not self.pub_stay_connected:
            self.loop.run_until_complete(self.close())
        return ret

    # END PUBLISH FEATURE

if __name__ == '__main__':
    c = SubNATS(NATS())
    c.subscribe(subject="help",queue="worker")
    c.start_loop()
