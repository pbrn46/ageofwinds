from PySide.QtGui import *
from PySide.QtCore import QEvent, Qt

from playScreen import PlayScreen
from inventoryScreen import InventoryScreen
from characterScreen import CharacterScreen


class Screens(QWidget):

    def __init__(self, game, parent=None):
        super(Screens, self).__init__(parent)
        self.game = game
        self.__current_screen = None

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
                was_visible = self.screens[k].isVisible()
                self.screens[k].setVisible(True)
                if not was_visible:
                    self.screens[k].grabKeyboard()
                    self.screens[k].toggled(True)  # Call toggled slot if was visible but not anymore.
                self.__current_screen = k
            else:
                was_visible = self.screens[k].isVisible()
                self.screens[k].setVisible(False)
                if was_visible:
                    self.screens[k].toggled(False)  # Call toggled slot if was visible but not anymore.

    def toggle_screen(self, screen_name):
        if self.current_screen_name() == screen_name:
            self.change_screen("play")
        else:
            self.change_screen(screen_name)

    def current_screen(self):
        return self[self.__current_screen]

    def current_screen_name(self):
        return self.__current_screen

