import math
import random

from PySide.QtCore import QPoint, QSize

from map.mapTileTypes import MapTileTypes
from direction import Direction


class GeneratorUtil:
    # List of relative positions that surround a position, for easy looping
    SurroundPoints = [
        QPoint(-1, -1),
        QPoint(0, -1),
        QPoint(1, -1),
        QPoint(-1, 0),
        QPoint(1, 0),
        QPoint(-1, 1),
        QPoint(0, 1),
        QPoint(1, 1),
    ]

    @staticmethod
    def layer_size(layer):
        maxX = -1
        maxY = -1
        for key in layer:
            if key[0] > maxX:
                maxX = key[0]
            if key[1] > maxY:
                maxY = key[1]
        maxX += 1
        maxY += 1
        return QSize(maxX, maxY)

    @staticmethod
    def overlay(base_layer, top_layer):
        """Overlay a top layer into the base layer, replacing the tile type in
        the base layer. top_layer may be a list, and will be overlayed starting
        at index 0."""
        new_layer = dict(base_layer)
        if isinstance(top_layer, list):
            for layer in top_layer:
                new_layer = GeneratorUtil.overlay(new_layer, layer)
        else:
            for key in top_layer:
                new_layer[key] = top_layer[key]
        return new_layer

    @staticmethod
    def offset(offset, layer):
        """Offset a layer by adding to all x and y values
        Args:
        offset (QPoint): Positive or negative point to offset the entire layer
        """
        new_layer = {}
        for key in layer:
            new_layer[key[0] + offset.x(), key[1] + offset.y()] = layer[key]
        return new_layer

    @staticmethod
    def random_pos(withinSize, includeBounds=True):
        """Return a random position (QPoint) based on a maximum size.
        :includeBounds: When false, it will exlude the boundary positions (up-
        left- bottom- right-most positions)
        """
        if includeBounds:
            return QPoint(
                random.randint(0, withinSize.width() - 1),
                random.randint(0, withinSize.height() - 1))
        else:
            return QPoint(
                random.randint(1, withinSize.width() - 2),
                random.randint(1, withinSize.height() - 2))

    @staticmethod
    def check_clearance(main_layer, over_layer, expand=False):
        """Check whether over_layer is obstructed in main_layer

        Args:
        main_layer (dict): Layer to check
        over_layer (dict): Layer, with positions relative to main_layer, to
        test.
        expand (bool): If true, will build walls around over_layer before
        checking

        Returns:
        True if the bottom of over_layer is just MapTileTypes.wall. False
        otherwise.
        """
        expanded_room = GeneratorUtil.add_walls(over_layer)
        for key in expanded_room:
            try:
                tile_type = main_layer[key]
            except KeyError:
                return False
            if tile_type != MapTileTypes.Wall:
                return False
        return True

    @staticmethod
    def add_walls(layer):
        """Returns the layer surrounded by MapTilesTypes.Wall. This is usually
        used for rooms."""
        new_layer = {}
        for key in layer:
            for point in GeneratorUtil.SurroundPoints:
                new_layer[key[0] + point.x(), key[1] + point.y()] = \
                    MapTileTypes.Wall
        new_layer = GeneratorUtil.overlay(new_layer, layer)
        return new_layer

    @staticmethod
    def get_random_pos_with_type(layer, tile_type):
        """Returns a random position of the layer that is the type of
        tile_type."""
        points = []
        for point, tile in layer.iteritems():
            if tile == tile_type:
                points.append(point)
        return points[random.randint(0, len(points) - 1)]

    @staticmethod
    def radial_tiles(layer, start_pos, radius):
        """Returns all tiles 'radius' (distance) apart from 'start_pos'. Starts
        at 0 for surrounding tiles."""
        new_layer = {}
        min = 0 - radius - 1
        max = radius + 1
        keys = []
        # Horizontal keys, inclusive
        keys = keys + [(x + start_pos.x(), min + start_pos.y())
                       for x in range(min, max + 1)]
        keys = keys + [(x + start_pos.x(), max + start_pos.y())
                       for x in range(min, max + 1)]
        # Vertical keys, exclusive
        keys = keys + [(min + start_pos.x(), y + start_pos.y())
                       for y in range(min + 1, max)]
        keys = keys + [(max + start_pos.x(), y + start_pos.y())
                       for y in range(min + 1, max)]

        for key in keys:
            if layer.get(key) is not None:
                new_layer[key] = layer[key]
        return new_layer

    @staticmethod
    def slice_layer(layer, start_pos, keep_direction):
        """Slice a layer and only keep things from that direction onwards
        start_pos (QPoint): Starting position
        keep_direction (Direction): The direction from start_pos to keep
        """
        new_layer = {}

        size = GeneratorUtil.layer_size(layer)

        # The line equation
        # y = mx + b, m = m(-y)/m(-x), b = y - mx
        # x = (y - b) / m
        def yOf(m, x, b):
            return (m * x) + b

        def xOf(m, y, b):
            return (y - b) / m

        incX = keep_direction[0]
        incY = keep_direction[1]

        if incX == 0:
            m = 0
        else:
            m = 0 - incY / incX

        b = start_pos.x() - (m * start_pos.y())

        for y in range(size.height()):
            if incY == 0:
                # startX = start_pos.x() + incX
                startX = start_pos.x()
            elif incX == 0:
                startX = 0
            else:
                startX = xOf(m, y, b)
            x = startX + incX
            while True:
                # print x, y, incX, incY
                if (x < 0 and incX < 0) \
                   or (x >= size.width() and incX >= 0):
                    break
                if incX == 0:
                    if y >= start_pos.y() and incY < 0:
                        break
                    if y <= start_pos.y() and incY > 0:
                        break
                key = (x, y)
                try:
                    new_layer[key] = layer[key]
                except KeyError:
                    pass
                x += incX + 1 - abs(incX)

        return new_layer

    @staticmethod
    def get_nearest_tiles(layer, start_pos, tile_type):
        """Get the nearest tiles of type 'tile_type' and return layer of
        positions of them"""
        new_layer = {}
        nearest_radius = -1
        layer_size = GeneratorUtil.layer_size(layer)
        for radius in range(max(layer_size.width(), layer_size.height())):
            radial_tiles = GeneratorUtil.radial_tiles(layer, start_pos, radius)
            for pos in radial_tiles:
                tile = radial_tiles[pos]
                if tile == tile_type:
                    real_radius = math.sqrt(
                        math.pow(pos[0] - start_pos.x(), 2) +
                        math.pow(pos[1] - start_pos.y(), 2))
                    if nearest_radius == -1 or real_radius < nearest_radius:
                        # print tile, nearest_radius
                        nearest_radius = real_radius
                        new_layer = {}
                        new_layer[pos] = tile
                    elif real_radius == nearest_radius:
                        new_layer[pos] = tile
            if len(new_layer) > 0:
                break
        return new_layer

    @staticmethod
    def get_room_walls(test_room):
        """Return a list of wall layers in the form of returnObj[Direction][x,
        y]"""
        room = GeneratorUtil.add_walls(test_room)
        u_wall = {}
        d_wall = {}
        l_wall = {}
        r_wall = {}
        umost_y = -1
        dmost_y = -1
        lmost_x = -1
        rmost_x = -1

        for key in room:
            if room[key] != MapTileTypes.Wall:
                continue
            x = key[0]
            y = key[1]
            if umost_y == -1 or y < umost_y:
                umost_y = y
                u_wall = {}
                u_wall[key] = room[key]
            elif y == umost_y:
                u_wall[key] = room[key]

            if dmost_y == -1 or y > dmost_y:
                dmost_y = y
                d_wall = {}
                d_wall[key] = room[key]
            elif y == dmost_y:
                d_wall[key] = room[key]

            if lmost_x == -1 or x < lmost_x:
                lmost_x = x
                l_wall = {}
                l_wall[key] = room[key]
            elif x == lmost_x:
                l_wall[key] = room[key]

            if rmost_x == -1 or x > rmost_x:
                rmost_x = x
                r_wall = {}
                r_wall[key] = room[key]
            elif x == rmost_x:
                r_wall[key] = room[key]

        u_wall_uniq = GeneratorUtil.remove_overlap(u_wall, l_wall)
        u_wall_uniq = GeneratorUtil.remove_overlap(u_wall_uniq, r_wall)
        d_wall_uniq = GeneratorUtil.remove_overlap(d_wall, l_wall)
        d_wall_uniq = GeneratorUtil.remove_overlap(d_wall_uniq, r_wall)
        l_wall_uniq = GeneratorUtil.remove_overlap(l_wall, u_wall)
        l_wall_uniq = GeneratorUtil.remove_overlap(l_wall_uniq, d_wall)
        r_wall_uniq = GeneratorUtil.remove_overlap(r_wall, u_wall)
        r_wall_uniq = GeneratorUtil.remove_overlap(r_wall_uniq, d_wall)

        returnDict = {}
        returnDict[Direction.Up] = u_wall_uniq
        returnDict[Direction.Down] = d_wall_uniq
        returnDict[Direction.Left] = l_wall_uniq
        returnDict[Direction.Right] = r_wall_uniq

        return returnDict

    @staticmethod
    def remove_overlap(base_layer, check_layer):
        """Returns a new base_layer without elements of the same position in
        check_layer"""
        new_layer = dict(base_layer)
        for key in check_layer:
            if key in new_layer:
                del new_layer[key]
        return new_layer

    # Use radial_tiles instead
    # def __get_surrounding_points(self, pos)

    @staticmethod
    def line(x1, y1, x2, y2):
        """Return a list<QPoint> of positions making a straight line"""
        line = []
        # x1, y1 = start_pos.x(), start_pos.y()
        # x2, y2 = end_pos.x(), end_pos.y()
        dx = x2 - x1
        dy = y2 - y1

        if (dx == 0):
            if (dy == 0):
                return [QPoint(x1, y1)]
            flip_line = GeneratorUtil.line(y1, x1, y2, x2)
            for point in flip_line:
                line.append(QPoint(point.y(), point.x()))
            return line

        step = 1 if x2 >= x1 else -1
        for x in range(x1, x2 + step, step):
            y = math.floor(y1 + dy * (x - x1) / dx)
            line.append(QPoint(x, y))

        return line
