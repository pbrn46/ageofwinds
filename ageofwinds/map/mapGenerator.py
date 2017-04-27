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

    Up = 0
    Down = 1

    def __init__(self, game):
        self.game = game
        self.mapLayer = {}
        self.start_pos = None
        self.size = QSize(0, 0)
        self.generator_pos = QPoint(0,0)
        self.prev_generator_direction = None
        self.prev_generator_type = None
        self.force_next_direction = False  # When true, next direction will follow previous direction

    def new_map(self, size):
        self.size = size
        self.__generate_all()
        return self.mapLayer

    def __generate_all(self):
        self.__blank_map()

        self.generator_pos = QPoint(random.randint(1, self.size.width() - 2), random.randint(1, self.size.height() - 2))
        self.start_pos = self.generator_pos

        """
        Generator Rules
        Paths:
            Max length: 50% of map
        Rooms:
            Max Size: 10x10
        """

        self.__set_tile(self.generator_pos, MapTileTypes.Floor)
        self.__add_random_path()
        self.__add_random_stairs(MapGenerator.Down)
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_stairs(MapGenerator.Down)
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_path()
        self.__add_random_door()
        self.__add_random_path()
        self.__add_random_stairs(MapGenerator.Down)

        # TODO: DEBUG Make a generator script
        # self.generator_pos = self.__add_door(GameUtil.transpose(self.generator_pos, Direction.Up))
        # self.generator_pos = GameUtil.transpose(self.generator_pos, Direction.Left, 4)
        # self.generator_pos = GameUtil.transpose(self.generator_pos, Direction.Up, 5)
        # self.generator_pos = self.__check_room_clearance(MapGenerator.RoomType_Rectangle, self.generator_pos, QSize(8, 5), True)

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

    def __add_random_door(self):
        """Put door in a random direction"""
        for i in range(100):
            direction = self.__random_direction(self.prev_generator_direction, no_diagonal=True)
            pos = GameUtil.transpose(self.generator_pos, direction, 1)
            if self.__in_map_limits(pos) and self.__check_buildable(pos):
                self.__add_door(pos)
                self.generator_pos = pos
                self.prev_generator_direction = direction
                break

    def __add_door(self, pos):
        self.__set_tile(pos, 8)
        return pos

    def __add_random_stairs(self, up_down):
        """Put stairs in a random direction"""
        for i in range(100):  # Try a bunch of times
            direction = self.__random_direction(self.prev_generator_direction, no_diagonal=True)
            pos = GameUtil.transpose(self.generator_pos, direction, 1)
            if self.__in_map_limits(pos) and self.__check_buildable(pos):
                valid = True
                self.__add_stairs(pos, up_down)
                self.generator_pos = pos
                self.prev_generator_direction = direction
                break

    def __add_stairs(self, pos, up_down):
        """
        
        :param pos: 
        :param up_down: MapGenerator.Up or MapGenerator.Down
        :return: 
        """
        if up_down == MapGenerator.Down:
            self.__set_tile(pos, 7)
        elif up_down == MapGenerator.Up:
            self.__set_tile(pos, 6)

    def __add_path(self, start_pos, direction, length):
        pos = start_pos
        if not self.__in_map_limits(pos):
            return pos

        for i in range(length):
            # Update previous adjacent tiles
            if i > 0:  # Do not place tile in starting pos
                self.__set_tile(pos, MapTileTypes.Floor)
                self.__update_diagonal_walls(pos, direction)

            next_pos = GameUtil.transpose(pos, direction)
            if self.__in_map_limits(next_pos):
                pos = next_pos
            else:
                break

        return pos

    def __random_direction(self, previous_direction=None, no_diagonal=False):
        """Return a random direction. If previous_direction is set, it prevents returning reverse of that direction
        
        :param previous_direction: If set, this prevents returning reverse of this direction, and also prevents the
            adjacent two directions.
        :param no_diagonal: 
        :return: 
        """
        r = Direction.random_direction(no_diagonal)
        if previous_direction is not None:
            near_directions = Direction.near_directions(Direction.reverse(previous_direction))
            print Direction.reverse(r), near_directions
            if r in near_directions:
                r = self.__random_direction(previous_direction, no_diagonal)
        return r

    def __add_random_path(self, no_diagonal=False):
        """Generate a random path. Return end position (inclusive)."""
        start_pos = self.generator_pos
        # while True:
        for i in range(100):
            while True:
                direction = self.__random_direction(self.prev_generator_direction, no_diagonal)
                # Prevent two diagonals in a row
                if not (Direction.is_diagonal(direction) and Direction.is_diagonal(self.prev_generator_direction)):
                    break

            length = random.randint(2, 30)
            end_pos = GameUtil.transpose(start_pos, direction, length - 1)

            if self.__in_map_limits(end_pos):
                if self.__check_buildable(GameUtil.transpose(start_pos, direction, 1), direction, length - 1):
                    self.__add_path(start_pos, direction, length)
                    self.prev_generator_direction = direction
                    self.force_next_direction = False
                    self.generator_pos = end_pos
                    return self.generator_pos
        else:
            print "Too many tries."
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

    def __check_buildable(self, start_pos, direction=None, length=1):
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
            if direction is not None:
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
        if pos.x() < 1:
            valid = False
        if pos.x() >= self.size.width() - 1:
            valid = False
        if pos.y() < 1:
            valid = False
        if pos.y() >= self.size.height() - 1:
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

