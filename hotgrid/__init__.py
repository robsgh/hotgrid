from .actions import HotGridAction


class HotGridElement:
    '''Simple wrapper class for an element in the HotGrid'''
    def __init__(self, name: str, icon_image: str, action: HotGridAction):
        self.name = name
        self.icon_image = icon_image
        self.action = action
        self.active = False

    # Call the action() function of the HotGridElement
    def activate(self) -> None:
        self.active = self.action.activate()


class HotGrid:
    ''' Collection of HotGridElements which perform commands for the user '''
    def __init__(self, grid_size: int = 10):
        self.size = 0
        self.grid_size = grid_size
        self._hotgrid = []

    ''' Add a new element to the HotGrid. When activated, the action will be ran '''
    def add(self, name, icon_image = None, action: HotGridAction = None) -> None:
        if not icon_image:
            icon_image = 'default.png'
        # Create a new element with the params and add it to the HotGrid
        new_ele = HotGridElement(name, icon_image, action)
        self.add_element(new_ele)

    ''' Add an element to the HotGrid '''
    def add_element(self, item) -> None:
        if self.size + 1 <= self.grid_size:
            self._hotgrid.append(item)

    ''' Call a HotGridElement's activate() function '''
    def activate(self, index) -> bool:
        if index < 0 or index > self.grid_size:
            return False
        self._hotgrid[index].activate()        

    ''' Get the current state of a HotGridElement '''
    def is_active(self, index) -> bool:
        if index < 0 or index > self.grid_size:
            return False
        return self._hotgrid[index].active

    ''' Get the grid list '''
    def get_hotgrid(self) -> list:
        return self._hotgrid
