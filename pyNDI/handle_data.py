import numpy as np
import quaternion
import struct

class transformation_data:
    def __init__(self):
        self.quaternion = quaternion.one
        self.translation = np.zeros((1,3))
        self.error = 0.0

class handle_data:
    Valid = 0x01
    Missing = 0x02
    Disabled = 0x03

    def __init__(self):
        self.status = handle_data.Disabled
        self.transformation_data = transformation_data()
        self.port_status = 0
        self.frame_number = 0
