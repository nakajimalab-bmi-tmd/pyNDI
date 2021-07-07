from ndiTrackingSystem import *
from PHRQ import *
from PVWR import *

class polaris(ndiTrackingSystem):
    """description of class"""

    def __init__(self):
        super().__init__()

    def initialize(self):
        super().initialize()
        # Set illuminator rate to 60 Hz in Polaris Spectra
        if self.ver.type_of_firmware == b'Polaris Spectra Control Firmware':
            print('This is spectra')
            
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

            # 6. check the port enabled
            port_status = self.command(PHSR(0x04))
            if port_status != None:
                print('The port is not enabled...')
                pass
            else:
                print('The wireless toll was enabled at ', ph)
