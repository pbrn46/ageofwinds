#!/usr/bin/env python

import math

from PySide.QtCore import *
from PySide.QtGui import *


class GameTime:
    def __init__(self, game):
        self.game = game
        self.currentTime = 0

    def add_time(self, seconds):
        # D 86400 H 3600 M 60 S 1
        self.currentTime += seconds

    def get_time_string(self):
        days = self.currentTime / 864000
        hours = self.currentTime % 86400 / 3600
        mins = self.currentTime % 3600 / 60
        secs = self.currentTime % 60

        return "%03dd %02dh %02dm %02ds" % (days, hours, mins, secs)
