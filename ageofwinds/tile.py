#!/usr/bin/env python


from PySide.QtCore import *
from PySide.QtGui import *


"""
zValues:
  0.0 - Map Terrain
  2.0 - Map structures (Doors / Stairs)
  4.0 - Items
  6.0 - Monsters
  8.0 - Main Character
  10.0 - Projectiles
"""


class Tile(object):
    # Enum for tile types. Also used for zValue
    TypeTerrain = 0
    TypeStructure = 2
    TypeItem = 4
    TypeMonster = 6
    TypeProtagonist = 8
    TypeProjectile = 10

    def __init__(self, game, tileNumber, pos, tileType):
        self.game = game
        self.worldMap = self.game.view.worldMap
        self.tileNumber = -1
        self.tileType = tileType

        self.isPassable = True
        self.stopBefore = False  # Stop before shift-run
        self.stopOnTop = False  # Stop on top during shift-run

        self.gfxItem = None  # Graphics view item attached to world map
        self.pos = pos

        self.set_tile_number(tileNumber)

    def set_tile_number(self, tileNumber):
        self.tileNumber = tileNumber
        self.update_pix(tileNumber)
        self.set_pos(self.pos)

    def get_tile_number(self):
        return self.tileNumber

    def set_gfx_item(self, gfxItem):
        self.gfxItem = gfxItem

    def center_cursor(self):
        QCursor.setPos(self.get_center_global_pos_px())

    def generate_tile(self, tile_number):
        pass
        # self.setPixmap(self.worldMap.tilePix[tileNumber])
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def update_pix(self, tile_number):
        if self.gfxItem:
            self.worldMap.gfxScene.removeItem(self.gfxItem)
            del self.gfxItem
        if self.tileType == Tile.TypeTerrain:
            pix = self.game.view.tilePix[tile_number]
        elif self.tileType == Tile.TypeProtagonist or self.tileType == Tile.TypeMonster:
            pix = self.game.view.spritePix[tile_number]
        self.gfxItem = self.worldMap.gfxScene.addPixmap(pix)
        self.gfxItem.setZValue(self.tileType)

    def set_pos(self, pos):
        self.pos = pos
        px_pos = self.worldMap.pos_to_px(pos)
        self.gfxItem.setPos(px_pos.x(), px_pos.y())

    def get_pos(self):
        return self.pos

    def get_center_view_pos_px(self):
        tile_width = self.game.view.tileSize.width()
        tile_height = self.game.view.tileSize.height()
        x_pos = tile_width * self.pos.x() + tile_width / 2
        y_pos = tile_height * self.pos.y() + tile_height / 2
        return QPoint(x_pos, y_pos)

    def get_center_global_pos_px(self):
        scene_pos = self.gfxItem.mapToScene(self.gfxItem.boundingRect().topLeft())
        view_pos = self.game.view.worldMap.gfxView.mapFromScene(scene_pos)
        global_pos = self.game.view.worldMap.gfxView.viewport().mapToGlobal(view_pos)

        tile_width = self.game.view.tileSize.width()
        tile_height = self.game.view.tileSize.height()

        global_center_pos = QPoint(global_pos.x() + tile_width / 2, global_pos.y() + tile_height / 2)
        return global_center_pos

    def ensure_visible(self):
        if self.game.view.worldMap.gfxView:
            pos_px = self.get_center_view_pos_px()
            self.game.view.worldMap.gfxView.ensureVisible(pos_px.x(), pos_px.y(), 1, 1, 100, 100)

    def center_on(self):
        if self.game.view.worldMap.gfxView:
            pos_px = self.get_center_view_pos_px()
            self.game.view.worldMap.gfxView.center_on(pos_px.x(), pos_px.y())

