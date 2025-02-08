from pyNDI.ndiTrackingSystem import *
from pyNDI.command.PHRQ import *
from pyNDI.command.PVWR import *
from pyNDI.command.SET import *
from pyNDI.command.GETINFO import *

class polaris(ndiTrackingSystem):
    """description of class"""

    def __init__(self):
        super().__init__()

    def get_optimal_baudrate(self):
        if self.ver.type_of_firmware == b'Polaris Spectra Control Firmware':
            return COMM.Bd_1228739

        return super().get_optimal_baudrate()
    def connect(self, port_name):
        super().connect(port_name)

    def initialize(self):
        super().initialize()
        if self.ver.type_of_firmware == b'Polaris Spectra Control Firmware':
            self.set_illuminator_rate()

    def set_illuminator_rate(self, rate = 2):
        try:
            print('setting illuminator rate to ', rate)
            self.command(SET('Param.Tracking.Illuminator Rate=' + str(rate)))
            return True
        except ValueError as e:
            print('failed to set illuminator rate to ', rate)
            return False

    def add_wireless_tool(self, srom_file):
        with open(srom_file, 'rb') as f:
            # 1. Free port handles that need to be freed
            port_status = self.command(PHSR(0x01))
            if port_status != None:
                for ph in port_status.keys():
                    self.command(PHF(ph))

            # 2. Assign a port handle to a tool
            ph = self.command(PHRQ())
            
            # 3. Load tool difinition file
            rom_data = f.read()
            rom_data = rom_data + bytes(64 - len(rom_data) % 64)
            address = 0
            while address < len(rom_data):
                segment = rom_data[address:address+64]
                self.command(PVWR(ph, address, segment))
                address += 64
                pass

            # 4. Initialize the handle
            self.command(PINIT(ph))

            # 5. Enable the handle
            self.command(PENA(ph))
            print('The wireless tool was enabled at ', ph)
