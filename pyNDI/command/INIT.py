from pyNDI.command.command_base import *

class INIT(command_base):
    def get_command(self):
        return 'INIT:'
