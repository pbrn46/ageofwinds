#!/usr/bin/env python

from PySide.QtGui import *
from PySide.QtCore import Qt, QEvent
from screens.screen import Screen
from screens.inventoryScreen_InventoryMdi import InventoryMdi
from screens.inventoryScreen_EquipmentSection import EquipmentSection


class InventoryScreen(Screen):
    def __init__(self, game, parent=None):
        """
        
        :param game: 
        :param parent: 
        """
        super(InventoryScreen, self).__init__(parent)
        self.game = game

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)

        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setSpacing(0)

        self.title = QLabel("Inventory")
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        font = self.title.font()
        font.setPointSize(18)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout1.addWidget(self.title)

        self.layout2 = QGridLayout()
        self.layout1.addLayout(self.layout2)

        self.equipment = EquipmentSection(self.game)
        self.layout2.addWidget(self.equipment, 0, 0)
        self.layout2.setColumnStretch(0, 50)

        self.inventory = InventoryMdi(self.game)
        self.layout2.addWidget(self.inventory, 0, 1)
        self.layout2.setColumnStretch(1, 50)

    def keyPressEvent(self, key_event):
        key = key_event.key()
        if key == 16777216:  # Esc
            self.game.view.change_screen("play")
        else:  # If not handled, event to focused widget
            self.focusWidget().keyPressEvent(key_event)
        return super(InventoryScreen, self).keyPressEvent(key_event)

    def toggled(self, visible_state):
        if visible_state:
            self.inventory.tileSubWindows()
            self.inventory.refresh_bags()
