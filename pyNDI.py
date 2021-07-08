### pyNDI library : pure python library for NDI tracking systems (Polaris, Aurora)
### ONOGI, Shinya, PhD, Department of Biomedical Information, Institute of Biomaterials and Bioengineering
### Tokyo Medical and Dental University
import time
from polaris import *

try:
    t = polaris()
    t.connect('/dev/ttyS1')
    t.initialize()
    t.activate_wired_tools()
    t.add_wireless_tool('8700340.rom')
    t.start_tracking()

    while True:
        data, stat = t.update()
        for k, v in data.items():
            if v.status == handle_data.Valid:
                print(k, v.transformation_data.translation)
            elif v.status == handle_data.Missing:
                print(k, "Missing")
            else:
                print(k, "Disabled")

        time.sleep(0.1)
except KeyboardInterrupt:
    t.stop_tracking()
    t.command(COMM(0, 0, 0, 0, 0))
except:
    pass