import codecs
from pyNDI.command.command_base import command_base

class GET(command_base):
    def __init__(self, arg):
        self.parameter_name = arg

    def get_command(self):
        return 'GET:' + self.parameter_name
    
    def read_reply(self):
        super().read_reply()
        reps =  codecs.decode(self.rep, 'utf-8').splitlines()
        return reps
