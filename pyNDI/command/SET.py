from pyNDI.command.command_base import command_base

class SET(command_base):
    def get_command(self, arg):
        return 'SET:' + arg
