from serial import *
from crc16 import *

class command_base:
    def get_command(self):
        raise NotImplementedError

    def pre_command(self, serial : Serial):
        pass

    def send_command(self, serial : Serial):
        serial.write(self.get_command().encode('ascii'))

    def recv_command(self, serial : Serial):
        buffer = serial.read_until(b'\r')[:-1]
        crc16.check(buffer)
        self.rep = buffer[:-4]
 
    def read_reply(self):
        ''' default reply is OKAY '''
        if self.rep == b'ERROR':
            raise ValueError(self.rep.decode('utf-8'), 'in', self.get_command())

    def post_command(self, serial):
        pass

