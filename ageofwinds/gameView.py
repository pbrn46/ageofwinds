#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from mainWindow import MainWindow


class GameView:
    def __init__(self, game):
        self.game = game
        self.mainWindow = None
        self.worldMap = None  # Shortcut to world map

        self.tilePix = []
        self.spritePix = []

        self.tileSize = QSize(32, 32)

        # Check if view scaling is necessary (high DPI environments)
        scrGeo = QApplication.desktop().screenGeometry()
        if scrGeo.width() > 1920 or scrGeo.height() > 1200:
            self.tileSize = QSize(48, 48)

        # Tile size in px

        self.load_pixmaps()

    def generate_view(self):
        self.mainWindow = MainWindow(self.game)
        self.set_world_map(
            self.mainWindow.playWindow.worldMap)  # Set as soon as world map is created in WorldMap() class now.
        self.worldMap.protagonist.ensure_visible()

    def set_world_map(self, world_map):
        self.worldMap = world_map

    def load_pixmaps(self):
        for x in range(500):
            pix = QPixmap("assets/tiles/%04d.png" % x)
            if not pix.isNull():
                pix = pix.scaled(self.tileSize, transformMode=Qt.SmoothTransformation)
            self.tilePix.append(pix)
        for x in range(500):
            pix = QPixmap("assets/sprites/%04d.png" % x)
            if not pix.isNull():
                pix = pix.scaled(self.tileSize, transformMode=Qt.SmoothTransformation)
            self.spritePix.append(pix)
