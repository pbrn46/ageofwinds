#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from mainWindow import MainWindow


class GameView:
    def __init__(self, game):
        self.game = game
        self.mainWindow = None
        self.dungeonMap = None  # Shortcut to world map, assigned when created in playScren

        self.tilePix = []
        self.spritePix = []

        self.tileSize = QSize(32, 32)

        # Check if view scaling is necessary (high DPI environments)
        scr_geo = QApplication.desktop().screenGeometry()
        if scr_geo.width() > 1920 or scr_geo.height() > 1200:
            self.tileSize = QSize(48, 48)

        # Tile size in px

        self.load_pixmaps()

    def generate_view(self):
        self.mainWindow = MainWindow(self.game)
        self.dungeonMap.protagonist.ensure_visible()

    def set_world_map(self, world_map):
        self.dungeonMap = world_map

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

    def change_screen(self, screen_name):
        """Shortcut function to self.mainWindow.screens.change_screen()"""
        self.mainWindow.screens.change_screen(screen_name)

    def toggle_screen(self, screen_name):
        """Shortcut function to self.mainWindow.screens.toggle_screen()"""
        self.mainWindow.screens.toggle_screen(screen_name)

