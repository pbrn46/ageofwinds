

class Direction:
    Left = 1 << 0
    Up = 1 << 1
    Right = 1 << 2
    Down = 1 << 3
    UpLeft = Up | Left
    UpRight = Up | Right
    DownRight = Down | Right
    DownLeft = Down | Left

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
