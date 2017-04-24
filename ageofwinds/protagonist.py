#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from sprite import Sprite


class Protagonist(Sprite):

    def __init__(self, game, pos):
        super(Protagonist, self).__init__(game, 230, pos, self.CategoryProtagonist)
        self.game.model.protagonist = self

        self.stats.set_current_hp(10)
        self.stats.set_max_hp(10)
        self.game.view.worldMap.explore_at(pos)

    # Override from Sprite
    def move_command(self, direction, isShift):
        super(Protagonist, self).move_command(direction, isShift)
        self.ensure_visible()

    # Override from Sprite
    def move(self, pos):
        moved = super(Protagonist, self).move(pos)
        if moved:
            self.game.view.worldMap.explore_at(pos)
            # TODO need to call some sort of tick function rather than add time
            self.game.model.gameTime.add_time(1)
            self.game.model.statsUpdateEvent()

        return moved
