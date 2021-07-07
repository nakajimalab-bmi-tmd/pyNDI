import threading
from serial import *
from COMM import *
from INIT import *
from PHF import *
from PHRQ import *
from PHSR import *
from PINIT import *
from PENA import *
from RESET import *
from TSTART import *
from TSTOP import *
from BX import *
from TX import *
from VER import *

class ndiTrackingSystem(object):
    """description of class"""
    def __init__(self):
        self.tracking = False
        self.serial = Serial()
        self.trackers = [{}, {}]
        self.system_status = [0, 0]
        self.read = 0
        self.write = 1

        self.ver = version_information()

    def command(self, cmd : command_base):
        cmd.pre_command(self.serial)
        cmd.send_command(self.serial)
        cmd.recv_command(self.serial)
        rep = cmd.read_reply()
        cmd.post_command(self.serial)
        return rep

    #def auto_connect(self):
    #    pass

    def connect(self, port_name):
        self.serial.port = port_name
        self.serial.baudrate = 9600
        self.serial.open()

    def initialize(self):
        self.command(RESET())
        self.ver = self.command(VER())
        print(self.ver.type_of_firmware)
        print(self.ver.ndi_serial_number)
        print(self.ver.copyright_information)
        self.command(COMM())
        self.command(INIT())

    def activate_wired_tools(self):
        # 1. Free port handles that need to be freed
        port_status = self.command(PHSR(0x01))
        if port_status != None:
            for ph in port_status.keys():
                self.command(PHF(ph))

        # 2. Initialize port handles that are not initialized
        port_status = self.command(PHSR(0x02))
        if port_status != None:
            for ph in port_status.keys():
                self.command(PINIT(ph))

        # 3. Enable port handles that are initialized, but not enabled 
        port_status = self.command(PHSR(0x03))
        if port_status != None:
            for ph in port_status.keys():
                self.command(PENA(ph))

    def start_tracking(self):
        self.command(TSTART())
        self.tracking = True
        self.tracking_thread = threading.Thread(target=self._tracking)
        self.tracking_thread.start()
        pass

    def stop_tracking(self):
        self.tracking = False
        self.tracking_thread.join()
        self.command(TSTOP())

    def _tracking(self):
        """loop and recieve tracking data"""
        try:
            while self.tracking:
                self.trackers[self.write], self.system_status[self.write] = self.command(BX())
                self.read, self.write = self.write, self.read
        except:
            self.tracking = False

    def update(self):
        return (self.trackers[self.read], self.system_status[self.read])

if __name__ == '__main__':
    tracker = ndiTrackingSystem()
    tracker.connect('COM8')
    tracker.initialize()
