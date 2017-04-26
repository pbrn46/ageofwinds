from inventoryItem import InventoryItem


class Inventory(list):
    def __init__(self, game, seq=()):
        super(Inventory, self).__init__(seq)
        self.game = game

    def create_item(self, name, sprite_id, parent=None):
        """Create an item. Returns index of created item."""
        item = InventoryItem()
        self.append(item)
        index = self.index(item)
        item.name = name
        item.icon = self.game.view.spritePix[sprite_id]
        item.parent = parent
        return index
