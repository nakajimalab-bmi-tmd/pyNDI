### polaris_tracking.py in pyNDI library : a sample polaris tracking for pyNDI
### ONOGI, Shinya, PhD, Department of Biomedical Information, Institute of Biomaterials and Bioengineering
### Tokyo Medical and Dental University

import time
from pyNDI.polaris import *
import keyboard
import logging

ndiLogger = logging.getLogger('pyNDI')
#ndiLogger.setLevel(logging.INFO)
ndiLogger.addHandler(logging.StreamHandler())

try:
    t = polaris()
    t.connect()   
    #t.connect('COM5')
    #t.command(RESET())
    #t.connect('/dev/ttyS1')
    t.initialize()
    t.activate_wired_tools()
    t.add_wireless_tool('8700340.rom')
    t.start_tracking()
 
    while not keyboard.is_pressed('space'):
        data, stat = t.update()
        for k, v in data.items():
            if v.status == handle_data.Valid:
                print(k, v.transformation_data.as_transform_matrix())
            elif v.status == handle_data.Missing:
                print(k, "Missing")

        time.sleep(0.1)

    t.stop_tracking()

except Exception as e:
    print("Error: ", e.args)
    pass