""" 
   crc16.py 
   ONOGI, Shinya, PhD, 2021
"""

class crc16:
    def append(data : bytes):
        crc = format(crc16.calc(data), '04X').encode('ascii')
        data += crc
        return data

    def check(data : bytes):
        if crc16.calc(data[:-4]) != int(data[-4:], 16):
            raise ValueError('crc error')

    def calc(data):
        oddparity = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
        crc = 0
        for d in data:
            d = (d^(crc&0xff))&0xff
            crc >>= 8
            if (oddparity[d & 0x0f] ^ oddparity[d >> 4]):
                crc = crc ^ 0xc001
            d <<= 6
            crc ^= d
            d <<= 1
            crc ^= d
        return crc
