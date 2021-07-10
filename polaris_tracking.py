### polaris_tracking.py in pyNDI library : a sample polaris tracking for pyNDI
### ONOGI, Shinya, PhD, Department of Biomedical Information, Institute of Biomaterials and Bioengineering
### Tokyo Medical and Dental University

import time
from pyNDI.polaris import *
import keyboard

try:
    t = polaris()
    t.connect('COM6')
    t.command(RESET())
    #t.connect('/dev/ttyS1')
    t.initialize()
    t.add_wireless_tool('8700340.rom')
    t.start_tracking()

    while not keyboard.is_pressed('escape'):
        data, stat = t.update()
        for k, v in data.items():
            if v.status == handle_data.Valid:
                print(k, v.transformation_data.translation)
            elif v.status == handle_data.Missing:
                print(k, "Missing")
            else:
                print(k, "Disabled")

        time.sleep(0.1)

    t.stop_tracking()
    t.command(COMM(0, 0, 0, 0, 0))            
except:
    pass