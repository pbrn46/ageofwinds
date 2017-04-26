#!/usr/bin/env python

from PySide.QtGui import *
from PySide.QtCore import Qt

from ageofwinds.screens.screen import Screen


class CharacterScreen(Screen):
    def __init__(self, game, parent=None):
        super(CharacterScreen, self).__init__(parent)
        self.game = game

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title = QLabel("Character")
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        font = self.title.font()
        font.setPointSize(18)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.test_widget = QWidget()
        self.layout.addWidget(self.test_widget)

        self.setLayout(self.layout)

    def keyPressEvent(self, key_event):
        key = key_event.key()
        if key == 16777216:  # Esc
            self.game.view.change_screen("play")
