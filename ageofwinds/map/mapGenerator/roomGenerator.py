# import math
import random

from map.mapTileTypes import MapTileTypes
from map.mapGenerator.generatorUtil import GeneratorUtil


class RoomGenerator:
    min_room_size = 3
    max_room_size = 10

    @staticmethod
    def generate_rooms(working_map, map_size):
        """Generate a list of absoulte-positioned rooms"""

        # Make a copy of the map to test clearances
        test_map = dict(working_map)

        # Stored rooms, in absolute positions
        abs_rooms = []
        for i in range(100):
            generator_pos = GeneratorUtil.random_pos(map_size, False)
            room = RoomGenerator.__generate_room(map_size)
            abs_room = GeneratorUtil.offset(generator_pos, room)
            room_clear = GeneratorUtil.check_clearance(test_map, abs_room)
            if room_clear:
                test_map = GeneratorUtil.overlay(test_map, abs_room)
                abs_rooms.append(abs_room)
        return abs_rooms

    @staticmethod
    def __generate_room(map_size):
        """Generate a room, and return it.
        A room is defined as a 2D list with MapTileTypes.Floor.
        """
        room = {}
        room_width = random.randint(
            RoomGenerator.min_room_size,
            RoomGenerator.max_room_size)
        room_height = random.randint(
            RoomGenerator.min_room_size,
            RoomGenerator.max_room_size)
        for x in range(room_width):
            for y in range(room_height):
                room[x, y] = MapTileTypes.Floor
        return room
