from command_base import *
import time

class RESET(command_base):   
    def send_command(self, serial : Serial):
        serial.send_break()
        time.sleep(5)

    def post_command(self, serial : Serial):
        settings = serial.get_settings()
        settings['baudrate'] = 9600
        settings['bytesize'] = 8
        settings['parity'] = 'N'
        settings['stopbits'] = 1
        settings['xonxoff'] = False
        settings['rtscts'] = False
        settings['timeout'] = None
        settings['write_timeout'] = None
        settings['inter_byte_timeout'] = None
        serial.apply_settings(settings)
