### aurora_tracking.py in pyNDI library : a sample aurora tracking for pyNDI
### ONOGI, Shinya, PhD, Department of Biomedical Information, Institute of Biomaterials and Bioengineering
### Tokyo Medical and Dental University

import time
from pyNDI.aurora import *
import keyboard

try:
    t = aurora()
    t.connect('COM10')
    t.command(RESET())
    #t.connect('/dev/ttyS1')
    t.initialize()
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
        time.sleep(0.05)

    t.stop_tracking()
    t.command(COMM(0, 0, 0, 0, 0))
except:
    pass