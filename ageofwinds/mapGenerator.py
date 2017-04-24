import random

from PySide.QtCore import *
from PySide.QtGui import *

from direction import Direction
from mapTile import MapTile
from mapTileTypes import MapTileTypes
from gameUtil import GameUtil


class MapGenerator:
    RoomType_Rectangle = 0
    RoomType_Round = 1
    RoomType_Cross = 2

    def __init__(self, game):
        self.game = game
        self.mapLayer = {}
        self.startPos = None
        self.size = QSize(0, 0)

    def new_map(self, size):
        self.size = size
        self.__generate_all()
        # self.__debugPrint()
        return self.mapLayer

    def __generate_all(self):
        self.__blank_map()

        self.startPos = QPoint(random.randint(0, self.size.width() -1), random.randint(0, self.size.height() - 1))

        """
        Generator Rules
        Paths:
            Max length: 50% of map
        Rooms:
            Max Size: 10x10
        
        """

        ret_pos = self.__add_random_path(self.startPos)
        ret_pos = self.__add_random_path(ret_pos)
        ret_pos = self.__add_random_path(ret_pos)

        # TODO: DEBUG Make a generator script
        ret_pos = self.__add_path(ret_pos, Direction.Down, 10)
        ret_pos = self.__add_path(ret_pos, Direction.Right, 5)
        ret_pos = self.__add_path(ret_pos, Direction.DownRight, 5)
        ret_pos = self.__add_path(ret_pos, Direction.Down, 3)  # After each diagonal, we must follow with a couple straight
        ret_pos = self.__add_path(ret_pos, Direction.DownLeft, 5)
        ret_pos = self.__add_path(ret_pos, Direction.Down, 3)
        ret_pos = self.__add_path(ret_pos, Direction.Right, 10)
        ret_pos = self.__add_path(ret_pos, Direction.UpRight, 5)
        ret_pos = self.__add_path(ret_pos, Direction.Up, 3)
        ret_pos = self.__add_path(ret_pos, Direction.UpLeft, 5)
        ret_pos = self.__add_door(GameUtil.transpose(ret_pos, Direction.Up))
        ret_pos = GameUtil.transpose(ret_pos, Direction.Left, 4)
        ret_pos = GameUtil.transpose(ret_pos, Direction.Up, 5)
        ret_pos = self.__check_room_clearance(MapGenerator.RoomType_Rectangle, ret_pos, QSize(8, 5), True)

    def __get_size(self):
        """Calculate the actual size of the current map."""
        width = len([i for i, v in enumerate(self.mapLayer.keys()) if v[1] == 0])
        height = len([i for i, v in enumerate(self.mapLayer.keys()) if v[0] == 0])
        return QSize(width, height)

    def __blank_map(self):
        self.mapLayer = {}
        for x in range(self.size.width()):
            for y in range(self.size.height()):
                self.mapLayer[x, y] = MapTileTypes.Wall

    def __set_tile(self, pos, tile_number):
        self.mapLayer[pos.x(), pos.y()] = tile_number

    def __get_tile(self, pos):
        return self.mapLayer[pos.x(), pos.y()]

    def __add_door(self, pos):
        self.__set_tile(pos, 8)
        return pos

    def __add_path(self, start_pos, direction, length):
        pos = start_pos
        for i in range(length):
            if 0 <= pos.x() < self.size.width() and 0 <= pos.y() < self.size.height():
                self.__set_tile(pos, MapTileTypes.Floor)

            # Update previous adjacent tiles
            if i > 0:
                self.__update_diagonal_walls(pos, direction)

            if i >= length - 1:
                return pos
            if direction & Direction.Up and pos.y() <= 0:
                return pos
            if direction & Direction.Down and pos.y() >= (self.size.height() - 1):
                return pos
            if direction & Direction.Left and pos.x() <= 0:
                return pos
            if direction & Direction.Right and pos.x() >= (self.size.width() - 1):
                return pos

            pos = GameUtil.transpose(pos, direction)

    def __random_direction(self):
        r = random.randint(0, 7)
        return Direction.from_int(r)

    def __add_random_path(self, start_pos):
        """Generate a random path. Return end position (inclusive)."""
        valid_tries = 0
        valid_path = False
        direction = Direction.Left
        length = 0
        while not valid_path:
            valid_path = True  # True until proven otherwise
            direction = self.__random_direction()
            length = random.randint(1, 30)
            end_pos = GameUtil.transpose(start_pos, direction, length - 1)
            # Todo: Check that path does not intersect with any other openings / objects
            if end_pos.x() < 0:
                valid_path = False
            elif end_pos.x() >= self.size.width():
                valid_path = False
            elif end_pos.y() < 0:
                valid_path = False
            elif end_pos.y() >= self.size.height():
                valid_path = False
            valid_tries += 1
            if valid_tries > 100:  # If tried many times and still not valid, just stop.
                break

        if valid_path:
            return self.__add_path(start_pos, direction, length)
        else:
            return False

    def __update_diagonal_walls(self, pos, direction):
        if direction & Direction.Up and direction & Direction.Left:
            self.__set_tile(GameUtil.transpose(pos, Direction.Down), MapTileTypes.DownLeftWall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Right), MapTileTypes.UpRightWall)
        if direction & Direction.Up and direction & Direction.Right:
            self.__set_tile(GameUtil.transpose(pos, Direction.Down), MapTileTypes.DownRightWall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Left), MapTileTypes.UpLeftWall)
        if direction & Direction.Down and direction & Direction.Left:
            self.__set_tile(GameUtil.transpose(pos, Direction.Up), MapTileTypes.UpLeftWall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Right), MapTileTypes.DownRightWall)
        if direction & Direction.Down and direction & Direction.Right:
            self.__set_tile(GameUtil.transpose(pos, Direction.Up), MapTileTypes.UpRightWall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Left), MapTileTypes.DownLeftWall)

    def __check_path_clearance(self, start_pos, direction, length):
        # TODO
        pass

    def __has_surrounding_clearance(self, pos, ignore_pos):
        """Returns true if adjacent tiles have a clearance"""
        # print([pos, wall_pos, prev_pos])
        st = self.__get_surrounding_tiles(pos)
        for tile in st:
            if not tile.pos == ignore_pos:
                # print tile.pos
                if tile.isPassable:
                    return True
        return False

    def __get_surrounding_tiles(self, pos):

        pos_list = [QPoint(x, y) for x in xrange(pos.x() - 1, pos.x() + 2)
                    for y in xrange(pos.y() - 1, pos.y() + 2)
                    if (
                        (pos.x() != x or pos.y() != y) and
                        (0 <= x < self.size.width()) and
                        (0 <= y < self.size.height())
                    )]
        tiles = [MapTile(self.game, self.mapLayer[item.x(), item.y()], item) for item in pos_list]
        return tiles

    def __add_room(self, room_type, start_pos, size=None):
        pos = None
        if room_type == MapGenerator.RoomType_Rectangle:
            for x in range(size.width()):
                for y in range(size.height()):
                    pos = QPoint(start_pos.x() + x, start_pos.y() + y)
                    self.__set_tile(pos, MapTileTypes.Floor)
        return pos

    def __check_room_clearance(self, room_type, start_pos, size=None, build_if_clear=False):
        # Returns False if there is anything but walls
        if room_type == MapGenerator.RoomType_Rectangle:
            for x in range(size.width()):
                for y in range(size.height()):
                    pos = QPoint(start_pos.x() + x, start_pos.y() + y)
                    tile = self.__get_tile(pos)
                    if tile != MapTileTypes.Wall:
                        if build_if_clear:
                            return start_pos
                        else:
                            return False

        if build_if_clear:
            return self.__add_room(room_type, start_pos, size)
        else:
            return True

    def __debug_print(self):
        s = ""
        for x in range(self.size.width()):
            for y in range(self.size.height()):
                tile_num = self.mapLayer[x, y]
                s += '%03d' % tile_num + ","
            s += '\n'
        print s
