from pyNDI.command.command_base import command_base

class TSTOP(command_base):
    def get_command(self):
        return 'TSTOP:'
