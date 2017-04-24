from PySide.QtGui import *

from ageofwinds.screens.playScreen import PlayScreen
from ageofwinds.screens.inventoryScreen import InventoryScreen
from ageofwinds.screens.characterScreen import CharacterScreen


class Screens(QWidget):

    def __init__(self, game, parent=None):
        super(Screens, self).__init__(parent)
        self.game = game
        self.current_screen = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.screens = {}

        self.screens.update({"play": PlayScreen(self.game)})
        self.main_layout.addWidget(self.screens["play"])

        self.screens.update({"inventory": InventoryScreen(self.game)})
        self.main_layout.addWidget(self.screens["inventory"])

        self.screens.update({"character": CharacterScreen(self.game)})
        self.main_layout.addWidget(self.screens["character"])

        self.change_screen("play")

    def __getitem__(self, item):
        return self.get_screen(item)

    def get_screen(self, screen_name):
        if screen_name in self.screens:
            return self.screens[screen_name]
        else:
            return None

    def change_screen(self, screen_name):
        for k, v in self.screens.iteritems():
            if k == screen_name:
                self.screens[k].setVisible(True)
                self.current_screen = k
            else:
                self.screens[k].setVisible(False)

