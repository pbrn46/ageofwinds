

class InventoryItem(object):
    def __init__(self):
        super(InventoryItem, self).__init__()
        self.name = ""
        self.description = ""
        self.type_id = 0
        self.stats = {}
        self.icon = None
        self.parent = None  # Items should have parent unless equipped or on the floor.
