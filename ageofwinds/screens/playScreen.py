#!/usr/bin/env python

from PySide.QtGui import *
from PySide.QtCore import QEvent

from map.dungeonMap import DungeonMap
from screens.screen import Screen
from mainToolbar import MainToolbar


class PlayScreen(Screen):
    def __init__(self, game, parent=None):
        super(PlayScreen, self).__init__(parent)
        self.game = game

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.toolbar = MainToolbar(self.game)
        # self.addToolBar(self.toolbar)
        self.layout.addWidget(self.toolbar)

        self.dungeonMap = DungeonMap(self.game)
        self.game.view.set_world_map(self.dungeonMap)  # Create shortcut to dungeonMap from game.view
        self.layout.addWidget(self.dungeonMap)

        self.setLayout(self.layout)

        self.dungeonMap.gfxView.installEventFilter(self)
        self.dungeonMap.installEventFilter(self)
        self.grabKeyboard()

    def keyPressEvent(self, key_event):
        if self.game.control.play_key_event(key_event):
            return True

    def mousePressEvent(self, mouse_event):
        if self.game.control.play_mouse_event(mouse_event):
            return True

