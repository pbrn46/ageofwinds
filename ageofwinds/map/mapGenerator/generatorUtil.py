import random
from PySide.QtCore import QPoint, QSize

from map.mapTileTypes import MapTileTypes
# from direction import Direction


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

        # Swap X and Y if our Y is 0
        # if incY == 0:
        #     incX, incY = incY, incX

        if incX == 0:
            m = 0
        else:
            m = 0 - incY / incX

        b = start_pos.x() - (m * start_pos.y())

        for y in range(size.height()):
            if incY == 0:
                startX = start_pos.x() + incX
            elif incX == 0:
                startX = 0
            else:
                startX = xOf(m, y, b)
            x = startX
            while True:
                print x, y
                if (x < 0 and incX < 0) \
                   or (x >= size.width() and incX > 0):
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

    # Use radial_tiles instead
    # def __get_surrounding_points(self, pos)

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
