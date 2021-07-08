from serial import *
from pyNDI.command.crc16 import *

class command_base:
    def get_command(self):
        raise NotImplementedError

    def pre_command(self, serial : Serial):
        pass

    def send_command(self, serial : Serial):
        buffer = crc16.append(self.get_command().encode('ascii')) + b'\r'
        #print ('sending ', buffer)
        serial.write(buffer)

    def recv_command(self, serial : Serial):
        buffer = serial.read_until(b'\r')[:-1]
        #print ('received', buffer)
        crc16.check(buffer)
        self.rep = buffer[:-4]
 
    def read_reply(self):
        ''' default reply is OKAY '''
        if self.rep == b'ERROR':
            raise ValueError(self.rep.decode('utf-8'), 'in', self.get_command())

    def post_command(self, serial):
        pass

