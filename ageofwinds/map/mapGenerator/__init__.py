
from PySide.QtCore import QPoint
from direction import Direction
# from gameUtil import GameUtil
from map.mapTileTypes import MapTileTypes
from map.mapGenerator.generatorUtil import GeneratorUtil
from map.mapGenerator.roomGenerator import RoomGenerator
from map.mapGenerator.pathGenerator import PathGenerator


class MapGenerator:
    def __init__(self, game):
        self.game = game

    def new_map(self, map_size):
        return self.__generate_all(map_size)

    def get_player_start_pos(self, map_layer):
        """Returns where player should start inside map_layer"""

        # Find a random floor tile and return the position
        point = GeneratorUtil.get_random_pos_with_type(
            map_layer,
            MapTileTypes.Floor)
        return QPoint(point[0], point[1])

    def __generate_all(self, map_size):
        """Generates the entire map

        The plan:
        - Fill map with walls / impassable
        - Generate a bunch of rooms
        - Generate paths between closest rooms
        - Add doors
        - Add stairs
        """

        gen_map = self.__blank_map(map_size)

        # Generate a bunch of rooms
        abs_rooms = RoomGenerator.generate_rooms(gen_map, map_size)
        gen_map = GeneratorUtil.overlay(gen_map, abs_rooms)

        abs_paths = PathGenerator.generate_paths(gen_map, map_size, abs_rooms)
        gen_map = GeneratorUtil.overlay(gen_map, abs_paths)

        # # --- DEBUG CODE HERE
        # #
        # # -- radial_tiles
        # test_layer = GeneratorUtil.radial_tiles(gen_map, QPoint(2, 2), 1)
        # for key in test_layer:
        #     test_layer[key] = MapTileTypes.DoorClosed
        # gen_map = GeneratorUtil.overlay(gen_map, test_layer)
        # #
        # # -- slice_layer
        # slice_pos = QPoint(6, 6)
        # test_layer = GeneratorUtil.slice_layer(
        #     gen_map, slice_pos, Direction.Up)
        # for key in test_layer:
        #     test_layer[key] = MapTileTypes.DoorClosed
        # test_layer[
        #     slice_pos.x(),
        #     slice_pos.y()] = MapTileTypes.DoorOpen
        # gen_map = GeneratorUtil.overlay(gen_map, test_layer)
        # #
        # # -- get_nearest_tile_pos
        # nearest_pos = QPoint(25, 25)
        # test_layer = GeneratorUtil.slice_layer(
        #     gen_map, nearest_pos, Direction.UpRight)
        # nearest_layer = GeneratorUtil.get_nearest_tiles(
        #     test_layer, nearest_pos, MapTileTypes.Floor)
        # for key in nearest_layer:
        #     nearest_layer[key] = MapTileTypes.DoorClosed
        # nearest_layer[
        #     nearest_pos.x(),
        #     nearest_pos.y()] = MapTileTypes.DoorOpen
        # gen_map = GeneratorUtil.overlay(gen_map, nearest_layer)
        # #
        # # -- get_room_walls
        # walls = GeneratorUtil.get_room_walls(abs_rooms[0])
        # for direction in walls:
        #     wall = walls[direction]
        #     for key in wall:
        #         gen_map[key] = MapTileTypes.DoorClosed

        return gen_map

    def __blank_map(self, map_size):
        """Return a blank map with wall tiles"""
        new_map = {}
        for x in range(map_size.width()):
            for y in range(map_size.height()):
                new_map[x, y] = MapTileTypes.Wall
        return new_map

    # def __add_stairs(self, pos, up_down):
    #     """Add a staircase
    #     Args:
    #     up_down (MapGenerator.Up or MapGenerator.Down)
    #     """
    #     if up_down == MapGenerator.Down:
    #         self.__set_tile(pos, 7)
    #     elif up_down == MapGenerator.Up:
    #         self.__set_tile(pos, 6)

    def __debug_print(self):
        s = ""
        for x in range(self.map_size.width()):
            for y in range(self.map_size.height()):
                tile_num = self.mapLayer[x, y]
                s += '%03d' % tile_num + ","
            s += '\n'
        print s
