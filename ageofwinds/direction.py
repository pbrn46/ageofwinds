

class Direction:
    Left = 1 << 0
    Up = 1 << 1
    Right = 1 << 2
    Down = 1 << 3
    UpLeft = Up | Left
    UpRight = Up | Right
    DownLeft = Down | Left
    DownRight = Down | Right

    Direction_Ints = [
        Left,
        Up,
        Right,
        Down,
        UpLeft,
        UpRight,
        DownLeft,
        DownRight
    ]
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
    def to_string(direction):
        return Direction.Direction_Strings[direction]
