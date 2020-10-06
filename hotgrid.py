import logging

class HotGridElement:
    def __init__(self, name, icon_image, action_func, toggle = False):
        self.name = name
        self.icon_image = icon_image
        self.action = action_func
        self.toggle = toggle

    def activate(self):
        logging.debug('{}: Activated (t={})'.format(self.name, self.toggle))
        self.action()
