#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *
from direction import Direction
from gameUtil import GameUtil


class GameControl:
    KeyModeMove = 0
    KeyModeDoorClose = 1  # Open and close doors (waiting for direction or mouse click)
    KeyModeDoorOpen = 2  # Open and close doors (waiting for direction or mouse click)
    KeyModeCast = 3  # Casting spells (waiting for direction or mouse click)
    KeyModeDisarm = 4  # Disarm Trap (waiting for direction or mouse click)

    def __init__(self, game):
        self.game = game
        self.keyMode = self.KeyModeMove
        self.isMouseTargeting = False
        self.castingSpell = None

    def quit(self):
        QApplication.closeAllWindows()

    def cancel_command(self):
        self.set_key_mode(GameControl.KeyModeMove)
        self.castingSpell = None
        self.isMouseTargeting = False

    def complete_command(self):
        pass

    def mouse_event(self, widget, event):
        if event.button() == Qt.LeftButton:
            if self.isMouseTargeting:
                self.confirm_user_cast_target()
        elif event.button() == Qt.MiddleButton:
            return True
        elif event.button() == Qt.RightButton:
            return True

        return False

    def key_event(self, widget, event):
        direction = None
        is_shift = event.modifiers() & Qt.ShiftModifier

        if event.key() == 16777216:  # Esc
            self.cancel_command()
            return True
        elif event.key() == 16777234:  # Left
            direction = Direction.Left
        elif event.key() == 16777235:  # Up
            direction = Direction.Up
        elif event.key() == 16777236:  # Right
            direction = Direction.Right
        elif event.key() == 16777237:  # Down
            direction = Direction.Down
        elif event.key() == 16777232:  # UpLeft
            direction = Direction.UpLeft
        elif event.key() == 16777233:  # DownLeft
            direction = Direction.DownLeft
        elif event.key() == 16777238:  # UpRight
            direction = Direction.UpRight
        elif event.key() == 16777239:  # DownRight
            direction = Direction.DownRight
        elif event.key() == 16777249:  # Ctrl
            pass
        elif event.key() == 16777248:  # Shift
            pass
        elif event.key() == 60:  # <, Stairs up
            # TODO
            print("TODO: Stairs up")
            return True
        elif event.key() == 62:  # >, Stairs down
            # TODO
            print("TODO: Stairs down")
            return True
        elif event.key() == 67:  # c, Close Door
            self.game.view.worldMap.protagonist.center_cursor()
            self.set_key_mode(GameControl.KeyModeDoorClose)
            return True
        elif event.key() == 68:  # d, Disarm Trap
            self.game.view.worldMap.protagonist.center_cursor()
            # TODO
            print("TODO: Disarm trap")
            return True
        elif event.key() == 79:  # o, Open Door
            self.game.view.worldMap.protagonist.center_cursor()
            self.set_key_mode(GameControl.KeyModeDoorOpen)
            return True
        else:
            print(5, "Unhandled key: %s" % (event.key()))

        if direction:
            if self.keyMode == GameControl.KeyModeMove:
                self.game.view.worldMap.protagonist.move_command(direction, is_shift)
            elif self.keyMode == GameControl.KeyModeDoorClose:
                self.close_door_command(direction)
            elif self.keyMode == GameControl.KeyModeDoorOpen:
                self.open_door_command(direction)
            return True

        return False

    def set_key_mode(self, key_mode):
        self.keyMode = key_mode
        cursor = None
        if key_mode == GameControl.KeyModeDoorClose:
            self.game.model.log("Pending action: Door close...")
            cursor = QCursor(Qt.CrossCursor)
        if key_mode == GameControl.KeyModeDoorOpen:
            self.game.model.log("Pending action: Door open...")
            cursor = QCursor(Qt.CrossCursor)
        if key_mode == GameControl.KeyModeCast:
            spell_name = self.castingSpell.get_name()
            self.game.model.log("Casting spell: %s..." % spell_name)
            cursor = QCursor(Qt.CrossCursor)

        if cursor:
            self.game.view.worldMap.gfxView.setCursor(cursor)
        else:
            self.game.view.worldMap.gfxView.unsetCursor()

    def start_user_cast_target(self, spell):
        # Can only start if no pending command
        if not self.isMouseTargeting:
            self.isMouseTargeting = True
            self.castingSpell = spell
            self.set_key_mode(GameControl.KeyModeCast)

    def confirm_user_cast_target(self):
        if self.isMouseTargeting:
            cursor_px_pos = self.game.view.worldMap.gfxView.mapFromGlobal(QCursor.pos())
            cursor_px_pos = self.game.view.worldMap.gfxView.mapToScene(cursor_px_pos)
            target_pos = self.game.view.worldMap.px_to_pos(cursor_px_pos)
            # tile = self.game.view.worldMap.getTilePx(cursor_px_pos)
            # TODO: Change to caster position
            self.castingSpell.cast(QPoint(1, 1), target_pos)
            self.cancel_user_cast_target()

    def cancel_user_cast_target(self):
        if self.isMouseTargeting:
            self.cancel_command()

    def close_door_command(self, direction):
        target_pos = GameUtil.transpose(self.game.view.worldMap.protagonist.get_pos(), direction)
        tile = self.game.view.worldMap.get_tile(target_pos)
        tile_number = tile.get_tile_number()
        if tile_number == 9:
            tile.set_tile_number(8)
            self.game.model.log("Door closed.")
        else:
            self.game.model.log("Nothing to close.")
        tile.center_cursor()
        self.set_key_mode(GameControl.KeyModeMove)

    def open_door_command(self, direction):
        target_pos = GameUtil.transpose(self.game.view.worldMap.protagonist.get_pos(), direction)
        tile = self.game.view.worldMap.get_tile(target_pos)
        tile_number = tile.get_tile_number()
        if tile_number == 8:
            tile.set_tile_number(9)
            self.game.model.log("Door opened.")
        else:
            self.game.model.log("Nothing to open.")
        tile.center_cursor()
        self.set_key_mode(GameControl.KeyModeMove)
