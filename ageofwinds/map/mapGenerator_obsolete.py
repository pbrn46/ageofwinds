
"""Just some old code backup, before the mapGenerator rewrite 2017-06-23"""

import random
import math

from PySide.QtCore import QSize, QPoint
from direction import Direction
from gameUtil import GameUtil
from map.mapTileTypes import MapTileTypes
from map.mapTile import MapTile


class MapGenerator:
    RoomType_Rectangle = 0
    RoomType_Round = 1
    RoomType_Cross = 2

    Up = 0
    Down = 1

    SurroundPoints = [QPoint(-1, -1),
                      QPoint(0, -1),
                      QPoint(1, -1),
                      QPoint(-1, 0),
                      QPoint(1, 0),
                      QPoint(-1, 1),
                      QPoint(0, 1),
                      QPoint(1, 1),
                      ]

    def __init__(self, game):
        self.game = game
        self.mapLayer = {}
        # start_pos is where the protagonist will be generated.
        self.start_pos = None
        self.size = QSize(0, 0)
        self.generator_pos = QPoint(0, 0)
        self.prev_generator_direction = None
        self.prev_generator_type = None
        # When true, next direction will follow previous direction
        self.force_next_direction = False

        self.min_room_size = 3
        self.max_room_size = None  # If None, it will be 50% of map width

    def new_map(self, size):
        self.size = size
        self.__generate_all()
        return self.mapLayer

    def __generate_all(self):
        """Generates the entire map
        Generator Rules
        Paths:
            Max length: 50% of map
        Rooms:
            Max Size: 10x10

        The plan:
        - Fill map with walls / impassable
        - Generate a bunch of rooms
        - Generate paths between closest rooms
        - Add doors
        - Add stairs
        """
        self.__blank_map()

        # Pick an arbitrary starting point.

        rooms = []
        # Generate a bunch of rooms
        for i in range(100):
            self.generator_pos = self.__random_pos()
            room = self.__generate_room()
            room_clear = self.__check_room_clearance(self.generator_pos, room)
            if room_clear:
                self.mapLayer = self.__overlay(
                    self.mapLayer,
                    self.__offset(self.generator_pos, room))
                rooms += room
                self.start_pos = self.generator_pos

    def __random_pos(self):
        """Return a random position (QPoint) based on map size, except the
        border"""
        return QPoint(
            random.randint(1, self.size.width() - 2),
            random.randint(1, self.size.height() - 2))

    # def __get_size(self):
    #     """Calculate the actual size of the current map."""
    #     width = len(
    #         [i for i, v in enumerate(self.mapLayer.keys()) if v[1] == 0])
    #     height = len(
    #         [i for i, v in enumerate(self.mapLayer.keys()) if v[0] == 0])
    #     return QSize(width, height)

    def __blank_map(self):
        """Clear map, and fill with wall tiles."""
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
        """Add a door at specified position."""
        self.__set_tile(pos, 8)
        return pos

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

    def __generate_paths(self, start_pos, direction, length):
        """Generate paths in between rooms"""
        pass
        # pos = start_pos
        # if not self.__in_map_limits(pos):
        #     return pos

        # for i in range(length):
        #     # Update previous adjacent tiles
        #     if i > 0:  # Do not place tile in starting pos
        #         self.__set_tile(pos, MapTileTypes.Floor)
        #         self.__update_diagonal_walls(pos, direction)

        #     next_pos = GameUtil.transpose(pos, direction)
        #     if self.__in_map_limits(next_pos):
        #         pos = next_pos
        #     else:
        #         break

        # return pos

    # def __random_direction(self, previous_direction=None, no_diagonal=False):
    #     """Return a random direction. If previous_direction is set, it
    #     prevents returning reverse of that direction
    #     :param previous_direction: If set, this prevents returning reverse of
    #         this direction, and also prevents the adjacent two directions.
    #     :param no_diagonal:
    #     :return:
    #     """
    #     r = Direction.random_direction(no_diagonal)
    #     if previous_direction is not None:
    #         near_directions = Direction.near_directions(
    #             Direction.reverse(previous_direction))
    #         print Direction.reverse(r), near_directions
    #         if r in near_directions:
    #             r = self.__random_direction(previous_direction, no_diagonal)
    #     return r

    # def __update_diagonal_walls(self, pos, direction):
    #     if direction & Direction.Up and direction & Direction.Left:
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Down),
    #             MapTileTypes.DownLeftWall,
    #             only_if_type=MapTileTypes.Wall)
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Right),
    #             MapTileTypes.UpRightWall,
    #             only_if_type=MapTileTypes.Wall)
    #     if direction & Direction.Up and direction & Direction.Right:
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Down),
    #             MapTileTypes.DownRightWall,
    #             only_if_type=MapTileTypes.Wall)
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Left),
    #             MapTileTypes.UpLeftWall,
    #             only_if_type=MapTileTypes.Wall)
    #     if direction & Direction.Down and direction & Direction.Left:
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Up),
    #             MapTileTypes.UpLeftWall,
    #             only_if_type=MapTileTypes.Wall)
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Right),
    #             MapTileTypes.DownRightWall,
    #             only_if_type=MapTileTypes.Wall)
    #     if direction & Direction.Down and direction & Direction.Right:
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Up),
    #             MapTileTypes.UpRightWall,
    #             only_if_type=MapTileTypes.Wall)
    #         self.__set_tile(
    #             GameUtil.transpose(pos, Direction.Left),
    #             MapTileTypes.DownLeftWall,
    #             only_if_type=MapTileTypes.Wall)

    # def __check_buildable(self, start_pos, direction=None, length=1):
    #     """Check if proposed path is only on wall."""
    #     cur_pos = start_pos
    #     clear = True
    #     for i in range(length):
    #         if self.__get_tile(cur_pos) != MapTileTypes.Wall:
    #             clear = False
    #             break
    #         for t in self.__get_surrounding_tiles(cur_pos):
    #             if start_pos != cur_pos and t.get_tile_number(
    #             ) != MapTileTypes.Wall:
    #                 clear = False
    #         # if not self.__has_surrounding_clearance(cur_pos, start_pos):
    #         #     clear = False
    #         if direction is not None:
    #             cur_pos = GameUtil.transpose(cur_pos, direction)
    #     return clear

    def __overlay(self, base_layer, top_layer):
        """Overlay a top layer into the base layer, replacing the tile type in
        the base layer"""
        new_layer = dict(base_layer)
        for key in top_layer:
            new_layer[key] = top_layer[key]
        return new_layer

    def __offset(self, offset, layer):
        """Offset a layer by adding to all x and y values
        :offset: QPoint
        """
        new_layer = {}
        for key in layer:
            new_layer[key[0] + offset.x(), key[1] + offset.y()] = layer[key]
        return new_layer

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
        pos_list = [
            QPoint(x, y)
            for x in xrange(pos.x() - 1, pos.x() + 2)
            for y in xrange(pos.y() - 1, pos.y() + 2)
            if ((pos.x() != x or pos.y() != y) and
                (0 <= x < self.size.width()) and (0 <= y < self.size.height()))
        ]
        tiles = [
            MapTile(self.game, self.mapLayer[item.x(), item.y()], item)
            for item in pos_list
        ]
        return tiles

    def __generate_room(self):
        """Generate a room, and return it.
        A room is defined as a 2D list with MapTileTypes.Floor.
        """
        room = {}
        max_room_width = math.floor(self.size.width() / 2)
        max_room_height = math.floor(self.size.height() / 2)
        room_width = random.randint(self.min_room_size, max_room_width)
        room_height = random.randint(self.min_room_size, max_room_height)
        for x in range(room_width):
            for y in range(room_height):
                room[x, y] = MapTileTypes.Floor

        return room

    def __expand_room(self, room):
        """Returns a room surrounded by MapTilesTypes.Wall"""
        new_room = {}
        for key in room:
            for point in self.SurroundPoints:
                new_room[key[0] + point.x(), key[1] + point.y()] = \
                    MapTileTypes.Wall
        new_room = self.__overlay(new_room, room)
        return new_room

    def __check_room_clearance(self, start_pos, room):
        # Returns False if there is anything but walls
        expanded_room = self.__expand_room(room)
        for key in expanded_room:
            try:
                tile_type = self.mapLayer[key[0] + start_pos.x(),
                                          key[1] + start_pos.y()]
            except KeyError:
                return False
            if tile_type != MapTileTypes.Wall:
                return False
        return True

    # def __in_map_limits(self, pos):
    #     """Check if a point is within map limits"""
    #     valid = True
    #     if pos.x() < 1:
    #         valid = False
    #     if pos.x() >= self.size.width() - 1:
    #         valid = False
    #     if pos.y() < 1:
    #         valid = False
    #     if pos.y() >= self.size.height() - 1:
    #         valid = False
    #     return valid

    def __debug_print(self):
        s = ""
        for x in range(self.size.width()):
            for y in range(self.size.height()):
                tile_num = self.mapLayer[x, y]
                s += '%03d' % tile_num + ","
            s += '\n'
        print s
