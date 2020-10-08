import subprocess
import keyboard
import platform


class HotGridAction:
    subclasses = []
    actions = []
    config_items  = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        HotGridAction.subclasses.append(cls)
        HotGridAction.actions.append(cls.action_name)
        HotGridAction.config_items.append(cls.config_items)

    ''' Activate the HotGridAction '''
    def activate(self):
        pass

    ''' Get the items necessary for web configuration '''
    def get_config_items(self):
        pass


class HotGridActionKeyboard(HotGridAction):
    action_name = 'Keyboard'
    config_items = [{'name': 'Enter macro action', 'field': 'command', 'type': 'text'}]

    def __init__(self, command: str, write: bool = False, toggle: bool = False):
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
    action_name = 'Open A Process'
    config_items = [{'name': 'Enter process name to start (one word)', 'field': 'processName', 'type': 'text'}]

    ''' HotGrid Action type to open up a process with a specified process name '''
    def __init__(self, processName: str):
        self.process = processName

    ''' Open process. Returns false always, since action cannot be toggled. '''
    def activate(self) -> bool:
        if platform.system() == 'Windows':
            subprocess.Popen('start {}'.format(self.process), shell=True)
        else:   
            subprocess.Popen('{}'.format(self.process), shell=True)  # this should work on bash, not confirmed yet
