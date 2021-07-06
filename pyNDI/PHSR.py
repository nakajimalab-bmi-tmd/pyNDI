from command_base import command_base

class PHSR(command_base):
    def __init__(self, option = 0):
        self.option = option
        self.handle_status = {}

    def get_command(self):
        return 'PHSR:{:02X}'.format(self.option)

    def read_reply(self):
        self.num_port_handles = int(self.rep[0:2], 16)
        index = 2
        for i in range(self.num_port_handles):
            handle = int(self.rep[index:index+2], 16)
            index += 2
            status = int(self.rep[index:index+3], 16)
            index += 3
            self.handle_status[handle] = status
        return self.handle_status
