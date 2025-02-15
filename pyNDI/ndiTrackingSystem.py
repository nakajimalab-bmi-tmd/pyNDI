import threading
from logging import getLogger, debug, info, warning, error
from serial import *
from pyNDI.command import *

class ndiTrackingSystem(object):
    """description of class"""
    def __init__(self):
        self.tracking = False
        self.serial = Serial(timeout=1)
        self.trackers = [{}, {}]
        self.system_status = [0, 0]
        self.read = 0
        self.write = 1
        #self.lock = threading.Lock()
        self.ver = version_information()

    def __del__(self):
        getLogger('pyNDI').debug('__del__')
        if self.tracking:
            self.stop_tracking()
        self.command(COMM(0, 0, 0, 0, 0))
        self.serial.close()

    def command(self, cmd : command_base):
        #self.lock.acquire()
        logger = getLogger('pyNDI')
        for i in range(3):
            try:
                cmd.pre_command(self.serial)
                cmd.send_command(self.serial)
                cmd.recv_command(self.serial)
                rep = cmd.read_reply()
                cmd.post_command(self.serial)
                return rep
            except ValueError as e:
                logger.error(e.args)
                if i == 2:
                    raise e
                continue

    #def auto_connect(self):
    #    pass

    def get_optimal_baudrate(self):
        return COMM.Bd_115200 # default

    def connect(self, port_name):
        self.serial.port = port_name
        self.serial.baudrate = 9600
        self.serial.bytesize = EIGHTBITS
        self.serial.parity = PARITY_NONE
        self.serial.stopbits = STOPBITS_ONE
        self.serial.timeout = 1
        self.serial.xonxoff = False
        self.serial.rtscts = False
        self.serial.dsrdtr = False
        self.serial.open()
 
    def initialize(self):
        self.initialize_system()

    def initialize_system(self, tried = 3):
        try:
            logger = getLogger('pyNDI')
            self.ver = self.command(VER())    
            logger.info(self.ver.type_of_firmware)
            logger.info(self.ver.ndi_serial_number)
            logger.info(self.ver.copyright_information)
            apirev = self.command(APIREV())
            logger.info(apirev)
            self.command(COMM(self.get_optimal_baudrate()))
            self.command(INIT())
        except:
            if tried > 0:
                logger.warning('retry to initialize')
                tried -= 1
                #self.command(RESET())
                self.initialize_system(tried)
            else:
                raise IOError('cannot connect to ', self.serial.port)

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
                tool_info = self.command(PHINF(ph))
                if tool_info.tool_type == b'08000000': # strober
                    continue
                self.command(PENA(ph))
                getLogger('pyNDI').info('Port {:02X} is enabled'.format(ph))
        pass

    def start_tracking(self):
        getLogger('pyNDI').info('Start tracking')
        self.command(TSTART())
        self.tracking = True
        # self.tracking_thread = threading.Thread(target=self._tracking)
        # self.tracking_thread.start()
        pass

    def stop_tracking(self):
        self.tracking = False
        # self.tracking_thread.join()
        self.command(TSTOP())
        getLogger('pyNDI').info('Stop tracking')

    def _tracking(self):
        """loop and receive tracking data"""
        try:
            while self.tracking:
                self.trackers[self.write], self.system_status[self.write] = self.command(BX(BX.TransformationData | BX.AllTransformation))
                self.read, self.write = self.write, self.read
        except Exception as e:
            print(e)
            self.tracking = False

    def update(self):
        self.trackers[self.read], self.system_status[self.read] = self.command(BX(BX.TransformationData | BX.AllTransformation))
        return (self.trackers[self.read], self.system_status[self.read])

