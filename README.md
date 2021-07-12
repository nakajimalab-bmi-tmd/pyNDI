# pyNDI: Communication library for Polaris and Aurora systems
**PyNDI** is a Python package that provides communication with Polaris and Aurora systems, Northern Digital Inc.

## Install
$> pip install --no-index --find-links=. pyNDI

## How to use it
See sample/polaris_tracking.py

## Internal design
I applied 'Command Pattern', which is one of the design patterns.
All commands were inherit from class command_base, which has common interfaces, pre_command, send_command, recv_command, read_reply, and post_command.
Command specific processes were implemented using override in respective derived command classes.

As the 'Command Pattern', 'command' function was simply implemented as:
    def command(self, cmd : command_base):
        cmd.pre_command(self.serial)
        cmd.send_command(self.serial)
        cmd.recv_command(self.serial)
        rep = cmd.read_reply()
        cmd.post_command(self.serial)
        return rep

When you need additional command implementations, you can simply add new derived command class without any changes in the present codes and add import the class.
