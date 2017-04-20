#!/usr/bin/env python

import csv
import time
import math

from PySide.QtCore import *
from PySide.QtGui import *

from mapTile import MapTile
from protagonist import Protagonist


class WorldMap(QWidget):
    def __init__(self, game, parent=None):
        super(WorldMap, self).__init__(parent)
        self.game = game
        self.game.view.set_world_map(self)
        start_time = time.time()

        self.viewMatrix = {}
        self.mapLayer = {}
        self.protagonist = None

        self.mapSize = None
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.gfxScene = QGraphicsScene()  # Scene to hold graphics
        self.gfxView = QGraphicsView()  # View to show scene
        # self.gfxView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.gfxView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gfxView.setScene(self.gfxScene)
        self.gfxView.installEventFilter(self)
        self.layout.addWidget(self.gfxView)

        self.generate_map()

        self.generate_protagonist()

        endTime = time.time()

        print("Map generated in: %s" % (endTime - start_time))

    # setMapSize()
    # size, QSize
    # Return None
    def set_map_size(self, size):
        self.mapSize = size

    def generate_map(self):
        # mapFile = open('test/testmap.csv', 'r')
        # mapCsv = csv.reader(mapFile, delimiter=",")
        # # self.mapLayer =
        # itemCount = 0
        # rowCount = 0
        # colCount = 0
        # for row in mapCsv:
        #     colCount = 0
        #     for item in row:
        #         try:
        #             item = int(item)
        #         except ValueError:
        #             item = 0
        #         self.mapLayer[colCount, rowCount] = item
        #         itemCount += 1
        #         colCount += 1
        #     rowCount += 1
        # self.setMapSize(QSize(colCount, rowCount))

        # TODO: DEBUG
        size = QSize(30, 20)
        self.mapLayer = self.game.model.mapGenerator.new_map(size)
        self.set_map_size(size)

        for y in range(self.mapSize.height()):
            for x in range(self.mapSize.width()):
                if (x, y) in self.mapLayer:
                    tileNumber = self.mapLayer[x, y]
                else:
                    tileNumber = 0
                self.set_tile_number(QPoint(x, y), tileNumber)

        self.explore_all()  # TODO: DEBUG Remove this

    def generate_protagonist(self, startPos=None):
        if startPos is None:
            startPos = self.game.model.mapGenerator.startPos
        self.protagonist = Protagonist(self.game, startPos)
        # self.protagonist.ensureVisible()

    def eventFilter(self, widget, event):
        if event.type() == QEvent.KeyPress:
            if self.game.control.key_event(widget, event):
                return True
        if event.type() == QEvent.MouseButtonPress:
            if self.game.control.mouse_event(widget, event):
                return True

        return QWidget.eventFilter(self, widget, event)

    def pos_to_px(self, pos):
        return QPoint(pos.x() * self.game.view.tileSize.width(), pos.y() * self.game.view.tileSize.height())

    def px_to_pos(self, pxPos):
        x = math.floor(pxPos.x() / self.game.view.tileSize.width())
        y = math.floor(pxPos.y() / self.game.view.tileSize.height())
        return QPoint(x, y)

    # setTileNumber()
    # Update tile at location, or create if not exist
    def set_tile_number(self, pos, tileNumber):
        tile = None
        try:  # Check for existence of tile
            self.viewMatrix[pos.x(), pos.y()].set_tile_number(tileNumber)
        except KeyError:  # Create if tile does not exist
            tile = MapTile(self.game, tileNumber, pos)  # , gfxItem)
            self.viewMatrix[pos.x(), pos.y()] = tile

    def get_tile_number(self, pos):
        return self.viewMatrix[pos.x(), pos.y()].get_tile_number()

    def get_tile(self, pos):
        """Get tile based on tile position"""
        try:
            return self.viewMatrix[pos.x(), pos.y()]
        except KeyError:
            return None

    def get_tile_px(self, pxPos):
        """Get tile based on px"""
        pos = self.px_to_pos(pxPos)
        return self.get_tile(pos)

    def is_passable_to(self, pos):
        if (pos.x(), pos.y()) in self.viewMatrix:
            if self.viewMatrix[pos.x(), pos.y()].isPassable:
                return True
        return False

    def is_stop_running_on_top(self, atPos):
        if self.viewMatrix[atPos.x(), atPos.y()].stopOnTop:
            return True
        return False

    def is_stop_running_before(self, toPos):
        if (toPos.x(), toPos.y()) in self.viewMatrix:
            if self.viewMatrix[toPos.x(), toPos.y()].stopBefore:
                return True
        return False

    def explore_at(self, pos):
        tile = self.get_tile(pos)
        if tile:
            tile.explore_here()
            return True
        else:
            return False

    def explore_all(self):
        for x in range(self.mapSize.width()):
            for y in range(self.mapSize.height()):
                self.get_tile(QPoint(x, y)).set_explored(True)

    def explore_segment(self, pos, radius):
        start_x = pos.x() - radius
        start_y = pos.y() - radius
        end_x = pos.x() + radius
        end_y = pos.y() + radius
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                tile = self.get_tile(QPoint(x, y))
                if tile:
                    tile.set_explored(True)

    def unexplore_all(self):
        for x in range(self.mapSize.width()):
            for y in range(self.mapSize.height()):
                self.get_tile(QPoint(x, y)).set_explored(False)
