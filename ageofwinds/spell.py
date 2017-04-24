#!/usr/bin/env python

import json
from PySide.QtCore import *
from PySide.QtGui import *


class Spell:

    def __init__(self, game, spellFile=None):
        self.game = game
        self.spellFile = spellFile
        # self.spellName = "" # Should be retrieved by function
        self.json = None

        if spellFile:
            self.load_spell(spellFile)

    def cast(self, start_pos=QPoint(-1, -1), target_pos=QPoint(-1, -1)):
        """Cast a spell."""
        """If cast() triggered by user without startPos and targetPos, begin cursor targeting"""

        target_required = self.get_attribute("targetRequired") == 'true'
        if target_required:
            if start_pos.x() < 0 or start_pos.y() < 0 or target_pos.x() < 0 or target_pos.y() < 0:
                # Begin targeting
                self.game.control.start_user_cast_target(self)
            else:
                self.cast_target_confirmed(start_pos, target_pos)
        else:
            self.cast_target_confirmed(start_pos, target_pos)

    def cast_target_confirmed(self, start_pos=QPoint(-1, -1), target_pos=QPoint(-1, -1)):
        self.handle_cast(start_pos, target_pos)
        self.game.model.log("Spell cast: %s" % self.get_name())

    def handle_cast(self, start_pos=QPoint(-1, -1), target_pos=QPoint(-1, -1)):
        actions = self.get_actions()
        for action in actions:
            self.handle_cast_actions(action, start_pos, target_pos)

    def handle_cast_actions(self, action, start_pos=QPoint(-1, -1), target_pos=QPoint(-1, -1)):
        if action == "exploreAll":
            # TODO: Should this expose hidden items like doors and traps?
            self.game.view.worldMap.explore_all()
        elif action == "unexploreAll":
            self.game.view.worldMap.unexplore_all()
        elif action == "exploreSegment":
            # TODO: Should this expose hidden items like doors and traps?
            radius = self.get_attribute("segmentRadius")
            if radius:
                radius = int(radius)
            self.game.view.worldMap.explore_segment(target_pos, radius)
        elif action == "regenerateMap":
            self.game.view.worldMap.generate_map()
            self.game.view.worldMap.protagonist.set_pos(self.game.model.mapGenerator.startPos)
            self.game.view.worldMap.protagonist.ensure_visible()

    def load_spell(self, spell_file):
        self.load_from_file("assets/spells/%s.json" % spell_file)
        self.spellFile = spell_file

    def load_from_file(self, file):
        f = open(file, 'r')
        self.json = json.load(f)

    def get_attribute(self, attribute):
        ret = None
        try:
            ret = self.json["spell"]["attributes"][attribute]
        except KeyError:
            print("Spell attribute not found: %s" % attribute)
        return ret

    def get_actions(self):
        ret = []
        try:
            ret = self.json["spell"]["actions"]
        except KeyError:
            print("Spell actions not found.")
        return ret

    def get_name(self):
        ret = ""
        try:
            ret = self.json["spell"]["name"]
        except KeyError:
            print("Spell name cannot be found.")
        return ret

    def get_description(self):
        ret = ""
        try:
            ret = self.json["spell"]["description"]
        except KeyError:
            print("Spell name cannot be found.")
        return ret
