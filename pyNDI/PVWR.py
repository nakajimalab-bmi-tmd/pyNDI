from command_base import command_base

class PVWR(command_base):
    def __init__(self, port_handle, address, data):
        self.port_handle = port_handle
        self.address = address
        self.data = data

    def get_command(self):
        return 'PVWR:{:02X}{:04X}'.format(self.port_handle, self.address) + self.data.hex().upper()
