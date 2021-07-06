from command_base import command_base

class version_information:
    def __init__(self):
        self.type_of_firmware = ''
        self.ndi_serial_number = ''
        self.characterization_date = ''
        self.freeze_tag = ''
        self.freeze_date = ''
        self.copyright_information = ''
        self.combined_firmware_revision = ''

class VER(command_base):
    SYSTEM_CONTROL_PROCESSOR = 0
    SYSTEM_CONTROL_UNIT_PROCESSOR = 3
    SYSTEM_CONTROL_PROCESSOR_WITH_ENHANCED_REVISION_NUMBER = 4
    COMBINED_FIRMWARE_REVISION_NUMBER = 5

    def __init__(self, option = 0):
        self.option = option
        self.ver_info = version_information()

    def get_command(self):
        return 'VER:{:02X}'.format(self.option)
    def read_reply(self):
        it = iter(self.rep.splitlines())
        if self.option == VER.COMBINED_FIRMWARE_REVISION_NUMBER:
            self.ver_info.combined_firmware_revision = next(it)
        else:
            self.ver_info.type_of_firmware = next(it)
            self.ver_info.ndi_serial_number = next(it)
            if self.option == VER.SYSTEM_CONTROL_PROCESSOR or self.option == VER.SYSTEM_CONTROL_PROCESSOR_WITH_ENHANCED_REVISION_NUMBER:
                self.ver_info.characterization_date = next(it)
            self.ver_info.freeze_tag = next(it)
            self.ver_info.freeze_date = next(it)
            self.ver_info.copyright_information = next(it)
        return self.ver_info
