#!/usr/bin/env python


from ageofwinds.map.mapGenerator import MapGenerator
from gameTime import GameTime
# from protagonist import Protagonist
from spellList import SpellList


class GameModel:
    def __init__(self, game):
        self.game = game
        self.gameTime = GameTime(game)
        self.mapGenerator = MapGenerator(game)
        self.protagonist = None
        self.statsUpdateEvent = None  # Should be in controller
        self.logList = None  # Should be in controller
        self.spellList = None

        self.make_spells()

    def make_spells(self):
        self.spellList = SpellList(self.game)

    def log(self, message):
        self.logList.addItem(message)
        self.logList.scrollToBottom()
