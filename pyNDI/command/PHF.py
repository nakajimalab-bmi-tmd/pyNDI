from pyNDI.command.command_base import command_base

class PHF(command_base):
    def __init__(self, port_handle):
        self.port_handle = port_handle

    def get_command(self):
        return 'PHF:{:02X}'.format(self.port_handle)
