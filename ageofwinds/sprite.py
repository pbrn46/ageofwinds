#!/usr/bin/env python

from ageofwinds.map.tile import Tile
from gameUtil import GameUtil
from spriteStats import SpriteStats


class Sprite(Tile):
    def __init__(self, game, tileNumber, pos, tileType):
        super(Sprite, self).__init__(game, tileNumber, pos, tileType)
        self.game = game
        self.stats = SpriteStats(game)
        self.canOpenDoors = True # TODO

    def move_command(self, direction, isShift):
        """Move command from user"""
        targetPos = GameUtil.transpose(self.pos, direction)
        self.move(targetPos)
        if isShift:
            finished = False
            while not finished:
                targetPos = GameUtil.transpose(self.pos, direction)
                if self.game.view.worldMap.is_stop_running_on_top(self.pos) \
                        or self.game.view.worldMap.is_stop_running_before(targetPos):
                    break
                finished = not self.move(targetPos)
        # self.game.view.worldMap.updateProtagonist()

    def move(self, pos):
        """Move position"""
        if self.game.view.worldMap.is_passable_to(pos):
            self.set_pos(pos)

            # Check door openings if over
            tileNumber = self.game.view.worldMap.get_tile_number(pos)
            if tileNumber == 8:
                self.game.view.worldMap.set_tile_number(pos, 9)
            return True
        else:
            return False

    def defend(self, attacker, attackPoints):
        """Defend an attack, and take hit points off"""
        # TODO
        pass

    def attack(self, defender, attackPoints):
        """Attack a defender"""
        # TODO
        pass
