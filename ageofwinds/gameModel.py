#!/usr/bin/env python


from ageofwinds.map.mapGenerator import MapGenerator
from gameTime import GameTime
from spellList import SpellList
from inventory import Inventory


class GameModel:
    def __init__(self, game):
        self.game = game
        self.gameTime = GameTime(self.game)
        self.mapGenerator = MapGenerator(self.game)
        self.protagonist = None
        self.statsUpdateEvent = None  # Should be in controller
        self.logList = None
        self.spellList = SpellList(self.game)
        self.inventory = Inventory(self.game)  # Should be bag inventory, referenced from equipment

    def log(self, message):
        self.logList.addItem(message)
        self.logList.scrollToBottom()
