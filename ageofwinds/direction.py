import random


class Direction:
    Left = 1 << 0
    Up = 1 << 1
    Right = 1 << 2
    Down = 1 << 3
    UpLeft = Up | Left
    UpRight = Up | Right
    DownLeft = Down | Left
    DownRight = Down | Right

    Direction_Ints = (  # Order is important!
        Left,
        UpLeft,
        Up,
        UpRight,
        Right,
        DownRight,
        Down,
        DownLeft
    )
    Direction_Strings = {
        Left: "Left",
        Up: "Up",
        Right: "Right",
        Down: "Down",
        UpLeft: "UpLeft",
        UpRight: "UpRight",
        DownLeft: "DownLeft",
        DownRight: "DownRight"
    }

    def __init__(self):
        pass

    @staticmethod
    def reverse(direction):
        if direction == Direction.Left:
            return Direction.Right
        if direction == Direction.Right:
            return Direction.Left
        if direction == Direction.Up:
            return Direction.Down
        if direction == Direction.Down:
            return Direction.Up
        if direction == Direction.UpLeft:
            return Direction.DownRight
        if direction == Direction.UpRight:
            return Direction.DownLeft
        if direction == Direction.DownLeft:
            return Direction.UpRight
        if direction == Direction.DownRight:
            return Direction.UpLeft

    @staticmethod
    def from_int(direction_int):
        """Return direction integer 0-7 as bit. Helper method for random generator"""
        return Direction.Direction_Ints[direction_int]

    @staticmethod
    def to_int(direction):
        """Return direction from integer 0-7."""
        try:
            return Direction.Direction_Ints.index(direction)
        except ValueError:
            raise ValueError

    @staticmethod
    def to_string(direction):
        return Direction.Direction_Strings[direction]

    @staticmethod
    def is_diagonal(direction):
        if direction == Direction.UpLeft:
            return True
        if direction == Direction.UpRight:
            return True
        if direction == Direction.DownLeft:
            return True
        if direction == Direction.DownRight:
            return True
        return False

    @staticmethod
    def near_directions(direction):
        """Returns a list with the direction as well as the two adjacent directions."""
        direction1 = direction

        direction2 = Direction.to_int(direction) - 1
        if direction2 < 0:
            direction2 = 7
        direction2 = Direction.from_int(direction2)

        direction3 = Direction.to_int(direction) + 1
        if direction3 > 7:
            direction3 = 0
        direction3 = Direction.from_int(direction3)

        return [direction1, direction2, direction3]


    @staticmethod
    def random_direction(no_diagonal=False):
        r = random.randint(0, 3 if no_diagonal else 7)
        return [Direction.Left, Direction.Up, Direction.Right, Direction.Down,
                Direction.UpLeft, Direction.UpRight, Direction.DownLeft, Direction.DownRight
                ][r]

