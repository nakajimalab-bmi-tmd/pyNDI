from pyNDI.command.command_base import *

class COMM(command_base):
    Bd_115200 = 5
    Bd_921600 = 6
    Bd_1228739 = 7 # Polaris Spectra USB only
    Bd_230400 = 0xA # Aurora only
    Databits_8 = 0
    Databits_7 = 1
    Parity_None = 0
    Parity_Odd = 1
    Parity_Even = 2
    StopBits_1 = 0
    StopBits_2 = 1
    Handshake_OFF = 0
    Handshake_ON = 1

    def __init__(self, baudrate = 5, databits = 0, parity = 0, stopbits = 0, handshake = 1):
        self.baudrate = baudrate
        self.databits = databits
        self.parity = parity
        self.stopbits = stopbits
        self.handshake = handshake
        
    def get_command(self):
        return 'COMM:{:X}{:X}{:X}{:X}{:X}'.format(self.baudrate, self.databits, self.parity, self.stopbits, self.handshake)

    def post_command(self, serial : Serial):
        settings = serial.get_settings()
        if self.baudrate == COMM.Bd_921600:
            settings['baudrate'] = 921600
        elif self.baudrate == COMM.Bd_115200:
            settings['baudrate'] = 115200
        elif self.baudrate == COMM.Bd_1228739:
            settings['baudrate'] = 19200 # Polaris API Guide, pp.59 
        if self.databits == COMM.Databits_8:
            settings['bytesize'] = 8
        else:
            settings['bytesize'] = 7
        if self.parity == COMM.Parity_None:
            settings['parity'] = 'N'
        elif self.parity == COMM.Parity_ODD:
            settings['parity'] = 'O'
        else: # COMM.Parity_EVEN
            settings['parity'] = 'E'
        if self.stopbits == COMM.StopBits_1:
            settings['stopbits'] = 1
        else: #COMM.StopBits_2
            settings['stopbits'] = 2
        if self.handshake == COMM.Handshake_OFF:
            settings['dsrdtr'] = False
        else: #COMM.Handshake_ON
            settings['dsrdtr'] = True
        serial.apply_settings(settings)
        time.sleep(0.1)

