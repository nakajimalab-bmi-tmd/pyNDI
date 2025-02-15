from logging import getLogger, debug, info, warning, error
from pyNDI.command.command_base import command_base

class PHINF(command_base):
    class tool_information:
        def __init__(self):
            self.tool_type = ''
            self.manufacturer_id = ''
            self.tool_revision = ''
            self.serial_number = ''
            self.port_status = ''
        
        def read_reply(self, rep):
            self.tool_type = rep[0:8]
            getLogger('pyNDI').debug('tool type %s', self.tool_type)
            self.manufacturer_id = rep[8:20]
            getLogger('pyNDI').debug('manufacturer id %s', self.manufacturer_id)
            self.tool_revision = rep[20:23]
            getLogger('pyNDI').debug('tool revision %s', self.tool_revision)
            self.serial_number = rep[23:31]
            getLogger('pyNDI').debug('serial number %s', self.serial_number)
            self.port_status = rep[31:33]
            getLogger('pyNDI').debug('port status %s', self.port_status)

    def __init__(self, port_handle):
        self.port_handle = port_handle
        self.tool_info = self.tool_information()

    def get_command(self):
        return 'PHINF:{:02X}'.format(self.port_handle)

    def read_reply(self):
        self.tool_info.read_reply(self.rep)
        return self.tool_info
    