#!/usr/bin/env python


from PySide.QtCore import *
from PySide.QtGui import *

from tile import Tile
from mapTileTypes import MapTileTypes


class MapTile(Tile):
    def __init__(self, game, tile_number, pos):
        super(MapTile, self).__init__(game, tile_number, pos, Tile.TypeTerrain)
        self.isPassable = True
        self.stopBefore = False  # Stop before shift-run
        self.stopOnTop = False  # Stop on top during shift-run
        self.visiblePix = self.gfxItem.pixmap()

        self.explored = False
        self.set_explored(False)

        self.assess_tile_properties(tile_number)

    def set_tile_number(self, tileNumber):
        super(MapTile, self).set_tile_number(tileNumber)
        self.assess_tile_properties(tileNumber)

    def set_explored(self, setTo):
        self.explored = setTo
        if self.explored:
            self.gfxItem.setVisible(True)
        else:
            self.gfxItem.setVisible(False)

    # assessTileProperties()
    # Check and assign properties to tile based on tile number
    def assess_tile_properties(self, tileNumber):
        if tileNumber == MapTileTypes.Wall:
            self.isPassable = False
            self.stopBefore = True
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.Floor:
            self.isPassable = True
            self.stopBefore = False
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.UpRightWall:
            self.isPassable = False
            self.stopBefore = True
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.DownRightWall:
            self.isPassable = False
            self.stopBefore = True
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.DownLeftWall:
            self.isPassable = False
            self.stopBefore = True
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.UpLeftWall:
            self.isPassable = False
            self.stopBefore = True
            self.stopOnTop = False
        elif tileNumber == MapTileTypes.StairsUp:
            self.isPassable = True
            self.stopBefore = False
            self.stopOnTop = True
        elif tileNumber == MapTileTypes.StairsDown:
            self.isPassable = True
            self.stopBefore = False
            self.stopOnTop = True
        elif tileNumber == MapTileTypes.DoorClosed:
            self.isPassable = True
            self.stopBefore = True
            self.stopOnTop = True
        elif tileNumber == MapTileTypes.DoorOpen:
            self.isPassable = True
            self.stopBefore = False
            self.stopOnTop = True

    def explore_here(self):
        pos = self.pos
        positions = []

        map_size = self.game.view.worldMap.mapSize
        max_x = map_size.width() - 1
        max_y = map_size.height() - 1

        start_x = pos.x() - 1
        start_y = pos.y() - 1
        for x in range(3):
            for y in range(3):
                t_x = start_x + x
                t_y = start_y + y
                if not (t_x < 0 or t_y < 0 or t_x > max_x or t_y > max_y):
                    positions.append(QPoint(t_x, t_y))

        for each_pos in positions:
            tile = self.worldMap.get_tile(each_pos)
            tile.set_explored(True)


