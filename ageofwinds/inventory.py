from inventorItem import InventoryItem


class Inventory(list):
    def __init__(self, game, seq=()):
        super(Inventory, self).__init__(seq)
        self.game = game

    def load_sample_data(self):
        for i in range(20):
            item = InventoryItem()
            self.append(item)
            index = self.index(item)
            item.name = "TestItem %s" % index
            item.icon = self.game.view.spritePix[66 + i]
            item.parent = 0

