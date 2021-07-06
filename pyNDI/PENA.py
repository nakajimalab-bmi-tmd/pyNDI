from command_base import command_base

class PENA(command_base):
    def __init__(self, port_handle, priority = 'D'):
        self.port_handle = port_handle
        self.priority = priority

    def get_command(self):
        return 'PENA:{:02X}{}'.format(self.port_handle, self.priority)

    def read_reply(self):
        super().read_reply()
        if rep[0:7] == b'Warning':
            print(self.rep.decode('utf-8'), 'in', self.get_command())

