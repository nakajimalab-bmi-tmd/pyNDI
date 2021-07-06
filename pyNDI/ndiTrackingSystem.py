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

class ndiTrackingSystem(object):
    """description of class"""
    def __init__(self):
        self.tracking = False
        self.serial = Serial()
        self.trackers = [{}, {}]
        self.system_status = [0, 0]
        self.read = 0
        self.write = 1

    def command(self, cmd : command_base):
        cmd.pre_command(self.serial)
        cmd.send_command(self.serial)
        cmd.recv_command(self.serial)
        cmd.read_reply(self.serial)
        cmd.post_command(self.serial)

    #def auto_connect(self):
    #    pass

    def connect(self, port_name):
        self.serial.setPort(port_name)
        self.serial.open()

    def initialize(self):
        try:
            self.command(COMM())
            self.command(INIT())
        except:
            self.command(RESET())
            self.command(COMM())
            self.command(INIT())
        else:
            pass

    def add_tool(self, srom_file):
        with open(srom_file, 'rb') as f:
            while True:
                block = f.read(64)
                if not block:
                    break
        pass

    def activate(self):
        # 1. Free port handles that need to be freed
        port_status = self.command(PHSR(0x01))
        for ph in port_status.keys():
            self.command(PHF(ph))

        # 2. Initialize port handles that are not initialized
        port_status = self.command(PHSR(0x02))
        for ph in port_status.keys():
            self.command(PINIT(ph))

        # 3. Enable port handles that are initialized, but not enabled 
        port_status = self.command(PHSR(0x03))
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
                self.trackers[write], self.system_status[write] = self.command(BX())
                read, write = write, read
        except:
            self.tracking = False

    def update(self):
        return (self.trackers[read], self.system_status[0])

if __name__ == '__main__':
    tracker = ndiTrackingSystem()
    tracker.connect('COM8')
    tracker.initialize()
