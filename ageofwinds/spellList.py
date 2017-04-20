#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from spell import Spell


class SpellList(list):

    def __init__(self, game):
        self.game = game

        # DEBUG
        tmp = Spell(game, "mapLevel")
        self.append(tmp)
        tmp = Spell(game, "testSpell")
        self.append(tmp)
        tmp = Spell(game, "mapSegment")
        self.append(tmp)
        tmp = Spell(game, "regenerateMap")
        self.append(tmp)

    def cast(self, spell_id):
        try:
            self[spell_id].cast()
        except IndexError:
            print("Spell ID not found in list: %s" % spell_id)
