#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *


class SpriteStats(dict):
    def __init__(self, game):
        super(SpriteStats, self).__init__()
        self.game = game
        self.__stats = {
            "current_hp": 0,
            "max_hp": 1,
            "current_mp": 0,
            "max_mp": 1
        }

    def __getitem__(self, item):
        return self.__stats[item]

    def __setitem__(self, key, value):
        self.__stats[key] = value

