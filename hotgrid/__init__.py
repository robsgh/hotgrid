from .actions import HotGridAction


class HotGridElement:
    '''Simple wrapper class for an element in the HotGrid'''
    def __init__(self, name: str, action: HotGridAction = HotGridAction(), icon_image: str = None, enabled: bool = True):
        self.name = name
        if not icon_image:
            self.icon_image = 'icons/default.png'
        else:
            self.icon_image = 'icons/' + icon_image
        self.action = action
        self.active = False
        self.enabled = enabled

    # Call the action() function of the HotGridElement
    def activate(self) -> None:
        self.active = self.action.activate()


class HotGrid:
    ''' Collection of HotGridElements which perform commands for the user '''
    def __init__(self, grid_size: int = 10):
        self.size = 0
        self.grid_size = grid_size
        self._free_slot = 0
        self._hotgrid = [HotGridElement('empty', enabled=False) for _ in range(grid_size)]

    ''' Add a new element to the HotGrid. When activated, the action will be ran '''
    def add(self, name: str, action: HotGridAction = None, icon_image: str = None, enabled: bool = True) -> None:
        # Create a new element with the params and add it to the HotGrid
        new_ele = HotGridElement(name=name, action=action, icon_image=icon_image, enabled=enabled)
        self.add_element(new_ele)

    ''' Add an element to the HotGrid '''
    def add_element(self, item: HotGridElement) -> None:
        if self.size + 1 <= self.grid_size:
            self._hotgrid[self._free_slot] = item
            self._free_slot += 1

    def modify_element(self, item: HotGridElement, index: int) -> None:
        if index < 0 or index > self.grid_size:
            return
        self._hotgrid[index] = item

    ''' Call a HotGridElement's activate() function '''
    def activate(self, index: int) -> bool:
        if index < 0 or index > self.grid_size:
            return False
        self._hotgrid[index].activate()        

    ''' Get the current state of a HotGridElement '''
    def is_active(self, index: int) -> bool:
        if index < 0 or index > self.grid_size:
            return False
        return self._hotgrid[index].enabled and self._hotgrid[index].active

    def is_enabled(self, index: int) -> bool:
        if index < 0 or index > self.grid_size:
            return False
        return self._hotgrid[index].active

    ''' Get the grid list '''
    def get_hotgrid(self) -> list:
        return self._hotgrid

    def get_actions(self) -> list:
        return HotGridAction.actions

    def get_config_items(self) -> list:
        return HotGridAction.config_items