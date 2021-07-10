from pyNDI.command.command_base import command_base

class TX(command_base):
    def __init__(self, option = 0x0001):
        self.option = option
    def get_command(self):
        return 'TX:{:04X}'.format(self.option)
    
    def read_reply(self):
        super().read_reply()
        print(self.rep)
        return self.rep

