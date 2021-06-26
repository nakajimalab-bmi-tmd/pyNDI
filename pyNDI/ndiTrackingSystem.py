import threading
from ndiSerial import ndiSerial


class ndiTrackingSystem(object):
    """description of class"""
    def __init__(self, *args, **kwargs):
        self.tracking = False

    def connect(self):
        pass

    def initialize(self):
        pass

    def add_tool(self, srom_file):
        with open(srom_file, 'rb') as f:
            while True:
                block = f.read(64)
                if not block:
                    break
        pass

    def activate(self):
        pass

    def start_tracking(self):
        self.tracking = True
        self.tracking_thread = threading.Thread(target=self._tracking)
        self.tracking_thread.start()
        pass

    def stop_tracking(self):
        self.tracking = False
        self.tracking_thread.join()
        pass

    def _tracking(self):
        """loop and recieve tracking data"""
        try:
            while self.tracking:
                pass
        except:
            self.tracking = False

    def update(self):
        pass

