from pyNDI.command.command_base import command_base

class TSTART(command_base):
    def get_command(self):
        return 'TSTART:'

