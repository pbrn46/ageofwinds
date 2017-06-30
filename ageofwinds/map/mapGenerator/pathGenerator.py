import math
import random

from PySide.QtCore import QPoint

from map.mapTileTypes import MapTileTypes
from map.mapGenerator.generatorUtil import GeneratorUtil
from direction import Direction


class PathGenerator:
    @staticmethod
    def generate_paths(map_layer, map_size, abs_rooms):
        new_map = dict(map_layer)
        abs_paths = []

        only_walls = {}  # Flattened layer of room walls to look through

        # Generate a flat layer with only walls
        for abs_room in abs_rooms:
            walls = GeneratorUtil.get_room_walls(abs_room)
            for direction in walls:
                wall = walls[direction]
                only_walls = GeneratorUtil.overlay(only_walls, wall)

        # Loop through each room
        for abs_room in abs_rooms:
            walls = GeneratorUtil.get_room_walls(abs_room)
            # Loop through each wall of the room
            for direction in walls:
                wall = walls[direction]
                wall_keys = wall.keys()
                # Randomize which wall tile to start from
                random.shuffle(wall_keys)
                # Loop through wall tiles
                for wall_key in wall_keys:
                    # Limit finding nearest room to the wall direciton
                    check_layer = GeneratorUtil.slice_layer(
                        only_walls,
                        QPoint(wall_key[0], wall_key[1]), direction)
                    # Find nearest wall tile from the "only wall" layer
                    nearest_tiles = GeneratorUtil.get_nearest_tiles(
                        check_layer,
                        QPoint(wall_key[0], wall_key[1]),
                        MapTileTypes.Wall)
                    # If there are nearest tiles found
                    if len(nearest_tiles) > 0:
                        tile_keys = nearest_tiles.keys()
                        # Since there may be more than one nearest tile,
                        # randomize.
                        random.shuffle(tile_keys)
                        # Loop through nearest tiles
                        for tile_key in tile_keys:
                            # Generate a path
                            path = PathGenerator.__gen_path(
                                QPoint(wall_key[0], wall_key[1]),
                                QPoint(tile_key[0], tile_key[1]),
                                direction)
                            if len(path) == 1:
                                raise "some shit"
                            # Overlay the path
                            new_map = GeneratorUtil.overlay(new_map, path)

                            # Add a door at the beginning of path, maybe
                            # if PathGenerator.__door_chance():
                            if True:
                                new_map[wall_key] = MapTileTypes.DoorClosed
                            # Add a door at the end of path, maybe
                            # if PathGenerator.__door_chance():
                            if True:
                                new_map[tile_key] = MapTileTypes.DoorOpen
                            # Break after first loop for only one path per wall

                            break
                        break

        return new_map

        return abs_paths

    @staticmethod
    def __gen_path(start_pos, end_pos, direction):
        path = {}
        x1, y1 = start_pos.x(), start_pos.y()
        x2, y2 = end_pos.x(), end_pos.y()
        dx = x2 - x1
        dy = y2 - y1
        # Check if line is straight (dots are ok too)
        if dx == 0 or dy == 0:
            path = PathGenerator.__gen_path_straight(x1, y1, x2, y2)
        else:
            path = PathGenerator.__gen_path_l(x1, y1, x2, y2, direction)
        return path

    @staticmethod
    def __gen_path_straight(x1, y1, x2, y2):
        path = {}
        line = GeneratorUtil.line(x1, y1, x2, y2)
        for point in line:
            path[point.x(), point.y()] = MapTileTypes.Floor
            # path[point.x(), point.y()] = MapTileTypes.DoorOpen
        return path

    @staticmethod
    def __gen_path_l(x1, y1, x2, y2, direction):
        """Make an L shaped path, starting with direction"""
        path = {}
        # dx = x2 - x1
        # dy = y2 - y1
        if direction == Direction.Up or direction == Direction.Down:
            next_path = PathGenerator.__gen_path_straight(x1, y1, x1, y2)
            path = GeneratorUtil.overlay(path, next_path)
            next_path = PathGenerator.__gen_path_straight(x1, y2, x2, y2)
            path = GeneratorUtil.overlay(path, next_path)
        else:
            next_path = PathGenerator.__gen_path_straight(x1, y1, x2, y1)
            path = GeneratorUtil.overlay(path, next_path)
            next_path = PathGenerator.__gen_path_straight(x2, y1, x2, y2)
            path = GeneratorUtil.overlay(path, next_path)
        return path

    @staticmethod
    def __door_chance():
        if random.randint(0, 8) < 1:
            return True
        return False
