from pyNDI.command.command_base import command_base

class descriptive_information:
    def __init__(self):
        self.user_parameter_name = ''
        self.value = ''
        self.type = ''
        self.attribute = ''
        self.minimum = ''
        self.maximum = ''
        self.enumertion = ''
        self.description = ''

class GETINFO(command_base):
    def __init__(self, arg):
        self.parameter_name = arg
        self.info = descriptive_information()

    def get_command(self):
        return 'GETINFO:' + self.parameter_name
    
    def read_reply(self):
        super().read_reply()
        it = iter(self.rep.split('='))
        it2 = it[1].split(';')
        self.info.user_parameter_name = it2[0]
        self.info.value = it2[1]
        self.info.type = it2[2]
        self.info.attribute = it2[3]
        self.info.minimum = it2[4]
        self.info.maximum = it2[5]
        self.info.enumertion = it2[6]
        self.info.description = it2[7]
        return self.info
