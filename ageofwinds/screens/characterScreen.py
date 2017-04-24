#!/usr/bin/env python

from PySide.QtGui import *


class CharacterScreen(QWidget):
    def __init__(self, game, parent=None):
        super(CharacterScreen, self).__init__(parent)
        self.game = game

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title = QLabel("Character")
        self.layout.addWidget(self.title)

        # self.worldMap = WorldMap(self.game)
        # self.layout.addWidget(self.worldMap)

        self.setLayout(self.layout)
