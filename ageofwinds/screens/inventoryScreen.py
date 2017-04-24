#!/usr/bin/env python

from PySide.QtGui import *
from ageofwinds.screens.inventoryScreen_InventoryMdi import InventoryMdi
from ageofwinds.screens.inventoryScreen_Equipment import EquipmentSection


class InventoryScreen(QWidget):
    def __init__(self, game, parent=None):
        super(InventoryScreen, self).__init__(parent)
        self.game = game

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)

        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setSpacing(0)

        self.title = QLabel("Inventory")
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout1.addWidget(self.title)

        self.layout2 = QGridLayout()
        self.layout1.addLayout(self.layout2)

        self.equipment = EquipmentSection()
        self.layout2.addWidget(self.equipment, 0, 0)
        self.layout2.setColumnStretch(0, 50)

        self.inventory = InventoryMdi()
        self.layout2.addWidget(self.inventory, 0, 1)
        self.layout2.setColumnStretch(1, 50)

