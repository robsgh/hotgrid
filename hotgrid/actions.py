import subprocess
import keyboard
import platform


class HotGridAction:
    def activate(self):
        pass


class HotGridActionKeyboard(HotGridAction):
    def __init__(self, command: str, write = False, toggle = False):
        self.command = command
        self.write = write
        self.toggle = toggle
        if toggle:
            self.active = False

    ''' Activate the keystroke command and return the state of the action (false always if not toggled). '''
    def activate(self) -> bool:
        if not self.toggle:
            if self.write:
                keyboard.write(self.command)
            else:
                keyboard.send(self.command)
            return False
        else:
            if self.active:
                keyboard.release(self.command)
            else:
                keyboard.press(self.command)
            self.active = not self.active

            return self.toggle and self.active


class HotGridActionOpenProcess(HotGridAction):
    ''' HotGrid Action type to open up a process with a specified process name '''
    def __init__(self, processName: str):
        self.process = processName

    ''' Open process. Returns false always, since action cannot be toggled. '''
    def activate(self) -> bool:
        if platform.system() == 'Windows':
            subprocess.Popen('start {}'.format(self.process), shell=True)
        else:   
            subprocess.Popen('{}'.format(self.process), shell=True)  # this should work on bash, not confirmed yet
