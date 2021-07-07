from command_base import command_base
from handle_data import *
from crc16 import crc16
import numpy as np
import quaternion
from serial import Serial
import struct

class BX(command_base):
    TransformationData = 0x0001
    ToolMarkerInformation = 0x0002
    SingleStrayActiveMarker = 0x0004
    MarkersOnTools = 0x0008
    AllTransformation = 0x0800
    StrayPassiveMarkers = 0x1000
    

    def __init__(self, tracking_mode = 0x0001):
        self.tracking_mode = tracking_mode
        self.handle_data = {}

    def get_command(self):
        return 'BX:{:04X}'.format(self.tracking_mode)

    def recv_command(self, serial : Serial):
        header = serial.read(2)
        if int.from_bytes(header[:2], 'little') != 0xA5C4:
            buffer = header + serial.read_until(expected = b'\r')[:-1]
            try:
                crc16.check(self.rep)
            except ValueError as crc_err:
                raise ValueError('Not binary reply and Invalid CRC in Error reply') from crc_err
            else:
                self.rep = buffer[:-4]
                raise ValueError(self.rep.decode('utf-8'), 'in', self.get_command())

        header += serial.read(4)
        #print(header.hex())
        if crc16.calc(header[:-2]) != int.from_bytes(header[-2:], 'little'):
            raise ValueError('CRC failure in header CRC')
        length = int.from_bytes(header[2:4], 'little')
        body = serial.read(length+2) # add binary crc
        #print(body.hex())
        if crc16.calc(body[:-2]) != int.from_bytes(body[-2:], 'little'):
            raise ValueError('CRC failure in header CRC')
        self.unpack_data(body[:-2])
    
    def unpack_data(self, buffer):
        index = 0
        num_handle = int(buffer[index])
        index += 1
        #print('num_handle =', num_handle)
        for i in range(num_handle):
            # <Handle><HandleStatus><TransformData><PortStatus><FrameNumber>
            handle = int(buffer[index])
            index += 1
            #print('\thandle:', handle)

            hdata = handle_data()
            hdata.status = int(buffer[index])
            index += 1
            #print('\thandle status:', hdata.status)

            if hdata.status != 0x04: #Disabled

                # <Reply Option 0001 Data>
                if self.tracking_mode & BX.TransformationData:
                    if hdata.status == 0x01: #handle status is "valid"
                        td = np.array(struct.unpack('<ffffffff', buffer[index:index+32]))
                        index += 32
                        hdata.transformation_data.quaternion = quaternion.from_float_array(td[0:4])
                        #print('\tQ:', hdata.transformation_data.quaternion)
                        hdata.transformation_data.translation = np.array(td[4:7])
                        #print('\tT:',hdata.transformation_data.translation)
                        hdata.transformation_data.error = td[7]
                    hdata.port_status, hdata.frame_number = struct.unpack('<II', buffer[index:index+8])
                    index += 8
                    #print('port status: ', hdata.port_status)
                    #print('frame number: ', hdata.frame_number)
                    #print(index, '/', len(buffer))
            self.handle_data[handle] = hdata

        # <System Status>
        self.system_status = int.from_bytes(buffer[index:index+2], 'little')
        #print('system status', self.system_status)
        index += 2
        #print(self.system_status)
        #print(index, '/', len(buffer))

    def read_reply(self):
        return (self.handle_data, self.system_status)
