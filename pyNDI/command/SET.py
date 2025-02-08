from pyNDI.command.command_base import command_base

class SET(command_base):
    def __init__(self, arg):
        self.parameter_name = arg
    def get_command(self):
        return 'SET:' + self.parameter_name
