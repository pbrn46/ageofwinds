import random

from PySide.QtCore import *
from ageofwinds.map.mapTileTypes import MapTileTypes

from ageofwinds.direction import Direction
from ageofwinds.gameUtil import GameUtil
from ageofwinds.map.mapTile import MapTile


class MapGenerator:
    RoomType_Rectangle = 0
    RoomType_Round = 1
    RoomType_Cross = 2

    def __init__(self, game):
        self.game = game
        self.mapLayer = {}
        self.startPos = None
        self.size = QSize(0, 0)
        self.generator_pos = QPoint(0,0)
        self.prev_generator_direction = None
        self.prev_generator_type = None

    def new_map(self, size):
        self.size = size
        self.__generate_all()
        return self.mapLayer

    def __generate_all(self):
        self.__blank_map()

        self.generator_pos = QPoint(random.randint(0, self.size.width() -1), random.randint(0, self.size.height() - 1))
        self.startPos = self.generator_pos

        """
        Generator Rules
        Paths:
            Max length: 50% of map
        Rooms:
            Max Size: 10x10
        
        """

        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()

        # TODO: DEBUG Make a generator script
        self.generator_pos = self.__add_door(GameUtil.transpose(self.generator_pos, Direction.Up))
        self.generator_pos = GameUtil.transpose(self.generator_pos, Direction.Left, 4)
        self.generator_pos = GameUtil.transpose(self.generator_pos, Direction.Up, 5)
        self.generator_pos = self.__check_room_clearance(MapGenerator.RoomType_Rectangle, self.generator_pos, QSize(8, 5), True)

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

    def __set_tile(self, pos, tile_number, only_if_type=-1):
        if (only_if_type == -1) or only_if_type == self.__get_tile(pos):
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

    def __add_random_path(self):
        """Generate a random path. Return end position (inclusive)."""
        start_pos = self.generator_pos
        end_pos = None
        valid_tries = 0
        valid_path = False
        direction = Direction.Left
        length = None
        while not valid_path:
            valid_path = True  # True until proven otherwise
            direction = self.__random_direction()
            if self.prev_generator_direction is not None:
                # Prevent two diagonals in a row
                while Direction.is_diagonal(direction) and Direction.is_diagonal(self.prev_generator_direction):
                    direction = self.__random_direction()

            length = random.randint(2, 30)
            end_pos = GameUtil.transpose(start_pos, direction, length - 1)
            if end_pos.x() < 0:
                valid_path = False
            if end_pos.x() >= self.size.width():
                valid_path = False
            if end_pos.y() < 0:
                valid_path = False
            if end_pos.y() >= self.size.height():
                valid_path = False
            if valid_path:
                if not self.__check_path_buildable(GameUtil.transpose(start_pos, direction, 1), direction, length - 1):
                    valid_path = False
            valid_tries += 1
            if valid_tries > 100:  # If tried many times and still not valid, just stop.
                break

        if valid_path:
            self.__add_path(start_pos, direction, length)
            self.prev_generator_direction = direction
            self.generator_pos = end_pos
            return self.generator_pos
        else:
            return False

    def __update_diagonal_walls(self, pos, direction):
        if direction & Direction.Up and direction & Direction.Left:
            self.__set_tile(GameUtil.transpose(pos, Direction.Down), MapTileTypes.DownLeftWall, only_if_type=MapTileTypes.Wall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Right), MapTileTypes.UpRightWall, only_if_type=MapTileTypes.Wall)
        if direction & Direction.Up and direction & Direction.Right:
            self.__set_tile(GameUtil.transpose(pos, Direction.Down), MapTileTypes.DownRightWall, only_if_type=MapTileTypes.Wall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Left), MapTileTypes.UpLeftWall, only_if_type=MapTileTypes.Wall)
        if direction & Direction.Down and direction & Direction.Left:
            self.__set_tile(GameUtil.transpose(pos, Direction.Up), MapTileTypes.UpLeftWall, only_if_type=MapTileTypes.Wall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Right), MapTileTypes.DownRightWall, only_if_type=MapTileTypes.Wall)
        if direction & Direction.Down and direction & Direction.Right:
            self.__set_tile(GameUtil.transpose(pos, Direction.Up), MapTileTypes.UpRightWall, only_if_type=MapTileTypes.Wall)
            self.__set_tile(GameUtil.transpose(pos, Direction.Left), MapTileTypes.DownLeftWall, only_if_type=MapTileTypes.Wall)

    def __check_path_buildable(self, start_pos, direction, length):
        """Check if proposed path is only on wall."""
        cur_pos = start_pos
        clear = True
        for i in range(length):
            if self.__get_tile(cur_pos) != MapTileTypes.Wall:
                clear = False
                break
            for t in self.__get_surrounding_tiles(cur_pos):
                if start_pos != cur_pos and t.get_tile_number() != MapTileTypes.Wall:
                    clear = False
            # if not self.__has_surrounding_clearance(cur_pos, start_pos):
            #     clear = False
            cur_pos = GameUtil.transpose(cur_pos, direction)
        return clear

    def __has_surrounding_clearance(self, pos, ignore_pos=None):
        """Returns true if adjacent tiles have a clearance"""
        # print([pos, wall_pos, prev_pos])
        st = self.__get_surrounding_tiles(pos)
        self.game.model.log(str(st))
        for tile in st:
            if ignore_pos is None or not tile.pos == ignore_pos:
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
                    if not self.__in_map_limits(pos):
                        return False
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

    def __in_map_limits(self, pos):
        """Check if a point is within map limits"""
        valid = True
        if pos.x() < 0:
            valid = False
        if pos.x() >= self.size.width():
            valid = False
        if pos.y() < 0:
            valid = False
        if pos.y() >= self.size.height():
            valid = False
        return valid

    def __debug_print(self):
        s = ""
        for x in range(self.size.width()):
            for y in range(self.size.height()):
                tile_num = self.mapLayer[x, y]
                s += '%03d' % tile_num + ","
            s += '\n'
        print s

