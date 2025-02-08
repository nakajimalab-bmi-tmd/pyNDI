from pyNDI.command.command_base import command_base

class APIREV(command_base):
    def get_command(self):
        return 'APIREV:'
    
    def read_reply(self):
        super().read_reply()
        return self.rep
