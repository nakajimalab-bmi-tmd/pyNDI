from serial import *
from crc16 import crc16

class command_base:
    def get_command(self):
        raise NotImplementedError

    def pre_command(self):
        pass

    def send_command(self, serial : Serial):
        serial.write(self.get_command().encode('ascii'))

    def recv_command(self, serial : Serial):
        buffer = serial.read_until(b'\r')[:-1]
        try:
            crc16.check(buffer)
            self.rep = buffer[:-4]
        except ValueError as e:
            print(e)

    def read_reply(self):
        ''' default reply is OKAY '''
        if self.rep == b'ERROR':
            raise ValueError(self.rep.decode('utf-8'), 'in', self.get_command())

    def post_command(self, serial):
        pass

class COMM(command_base):
    def __init__(self, baudrate, data, handshake):
        self.baudrate = baudrate
        self.data = data
        self.handshake = handshake

    def get_command(self):
        return 'COMM:{}{:03d}{}'.format(self.baudrate, self.data, self.handshake)

    def post_command(self, serial):
        return super().post_command()

class INIT(command_base):
    def get_command(self):
        return 'INIT:'

class PHRQ(command_base):
    def get_command(self):
        return 'PHRQ:*********1****'
    def read_reply(self):
        super().read_reply()
        if len(rep) != 2:
            raise ValueError
        return int(rep, 16)

class PVWR(command_base):
    def __init__(self, port_handle, rom_file):
        self.port_handle = port_handle
        self.rom_file = rom_file
        self.address = 0
        self.rom_data = bytes(1024)
        with open(rom_file, 'rb') as f:
            pass

    def get_command(self):
        hex_data = ''
        for i in range(64):
            hex_data += '{:02X}'.format(self.rom_data[self.address + i])
        return 'PVWR:{:02X}{:04X}'.format(self.port_handle, self.address) + hex_data

class PENA(command_base):
    def __init__(self, port_handle, priority = 'D'):
        self.port_handle = port_handle
        self.priority = priority

    def get_command(self):
        return 'PENA:{:02Xc}'.format(self.port_handle, self.priority)

class PINIT(command_base):
    def __init__(self, port_handle):
        self.port_handle = port_handle

    def get_command(self):
        return 'PINIT:{:02X}'.format(self.port_handle)

class TSTART(command_base):
    def get_command(self):
        return 'TSTART:'

class TSTOP(command_base):
    def get_command(self):
        return 'TSTOP:'

class TX(command_base):
    def get_command():
        return 'TX:'

class BX(command_base):
    def get_command():
        return 'BX'

def pre_command(serial: Serial, cmd):
    pass

def send_command(serial: Serial, cmd):
    buffer = cmd.get_command().encode('ascii')
    crc = format(crc16(buffer), '04X').encode('ascii')
    buffer += crc + b'\r'
    serial.write(buffer)
    pass

def recv_command(serial: Serial, cmd):
    buffer = serial.read_until(b'\r')
    pass

def post_command(serial: Serial, cmd):
    pass

def command(serial : Serial, cmd):
    pre_command(serial, cmd)
    send_command(serial, cmd)
    recv_command(serial, cmd)
    post_command(serial, cmd)
    pass
