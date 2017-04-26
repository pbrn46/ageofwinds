#!/usr/bin/env python

from ageofwinds.map.tile import Tile
from gameUtil import GameUtil
from spriteStats import SpriteStats


class Sprite(Tile):
    def __init__(self, game, tileNumber, pos, tileType):
        super(Sprite, self).__init__(game, tileNumber, pos, tileType)
        self.game = game
        self.stats = SpriteStats(game)
        self.canOpenDoors = True  # TODO

    # def move_command(self, direction, is_shift):
    #     """Move command from user"""
    #     targetPos = GameUtil.transpose(self.pos, direction)
    #     self.move(targetPos)
    #     if is_shift:
    #         finished = False
    #         while not finished:
    #             targetPos = GameUtil.transpose(self.pos, direction)
    #             if self.game.view.dungeonMap.is_stop_running_on_top(self.pos) \
    #                     or self.game.view.dungeonMap.is_stop_running_before(targetPos):
    #                 break
    #             finished = not self.move(targetPos)

    def move(self, pos):
        """Move position"""
        if self.game.view.dungeonMap.is_passable_to(pos):
            self.set_pos(pos)

            # Check door openings if over
            tile_number = self.game.view.dungeonMap.get_tile_number(pos)
            if tile_number == 8:
                self.game.view.dungeonMap.set_tile_number(pos, 9)
            return True
        else:
            return False

    def defend(self, attacker, attack_points):
        """Defend an attack, and take hit points off"""
        # TODO
        pass

    def attack(self, defender, attack_points):
        """Attack a defender"""
        # TODO
        pass
