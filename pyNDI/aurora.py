from pyNDI.ndiTrackingSystem import *

class aurora(ndiTrackingSystem):
    def get_optimal_baudrate(self):
        return COMM.Bd_921600
