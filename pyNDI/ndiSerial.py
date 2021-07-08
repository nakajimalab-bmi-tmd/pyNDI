from serial import *
### pySerial https://pythonhosted.org/pyserial/

class ndiSerial:
    LF = b'\n'
    CR = b'\r'

    def __init__(self):
        self.serial = Serial()


    def send(self, arg):
        data = arg.encode('ascii')
        crc = format(ndiSerial.crc16(data), '04X').encode('ascii')
        data += crc +self.CR
        self.serial.write(data)
        print(data)
        pass

    def recv(self):
        data = self.serial.read_until(self.CR)
        print(data)
        pass

    def recv_binary(self, size):
        data = s.read(size)

### --- ###

if __name__ == '__main__':
    serial = ndiSerial()
    serial.serial.port = 'COM8'
    serial.serial.open()
    serial.send('RESET')
    serial.recv()
    pass

