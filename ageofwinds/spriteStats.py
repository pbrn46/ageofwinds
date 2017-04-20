#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *


class SpriteStats:

    def __init__(self, game):
        self.game = game
        self.currentHp = 0
        self.currentMp = 0
        self.maxHp = 0
        self.maxMp = 0

    def set_current_hp(self, hp):
        self.currentHp = hp

    def set_current_mp(self, mp):
        self.currentMp = mp

    def set_max_hp(self, hp):
        self.maxHp = hp

    def set_max_mp(self, mp):
        self.maxMp = mp
