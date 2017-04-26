#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from sprite import Sprite
from gameUtil import GameUtil

class Protagonist(Sprite):
    def __init__(self, game, pos):
        super(Protagonist, self).__init__(game, 230, pos, self.CategoryProtagonist)
        self.game.model.protagonist = self

        self.game.view.dungeonMap.explore_at(pos)

    # Override from Sprite
    def move_command(self, direction, is_shift):
        """Move command from user"""
        target_pos = GameUtil.transpose(self.pos, direction)
        self.move(target_pos)
        if is_shift:
            finished = False
            while not finished:
                target_pos = GameUtil.transpose(self.pos, direction)
                if self.game.view.dungeonMap.is_stop_running_on_top(self.pos) \
                        or self.game.view.dungeonMap.is_stop_running_before(target_pos):
                    break
                finished = not self.move(target_pos)
        # super(Protagonist, self).move_command(direction, is_shift)
        self.ensure_visible()

    # Override from Sprite
    def move(self, pos):
        moved = super(Protagonist, self).move(pos)
        if moved:
            self.game.view.dungeonMap.explore_at(pos)
            self.game.control.game_tick()
        return moved
