from pyNDI.command.command_base import command_base

class PHRQ(command_base):
    def get_command(self):
        return 'PHRQ:*********1****'

    def read_reply(self):
        super().read_reply()
        if len(self.rep) != 2:
            raise ValueError
        return int(self.rep, 16)

