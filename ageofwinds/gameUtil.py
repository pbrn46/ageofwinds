from PySide.QtCore import QPoint
from direction import Direction


class GameUtil:
    @staticmethod
    def transpose(pos, direction, length=1):
        targetPos = QPoint(pos.x(), pos.y())

        if direction == Direction.Left:
            targetPos.setX(targetPos.x() - length)
        elif direction == Direction.Up:
            targetPos.setY(targetPos.y() - length)
        elif direction == Direction.Right:
            targetPos.setX(targetPos.x() + length)
        elif direction == Direction.Down:
            targetPos.setY(targetPos.y() + length)
        elif direction == Direction.DownLeft:
            targetPos.setX(targetPos.x() - length)
            targetPos.setY(targetPos.y() + length)
        elif direction == Direction.UpLeft:
            targetPos.setX(targetPos.x() - length)
            targetPos.setY(targetPos.y() - length)
        elif direction == Direction.DownRight:
            targetPos.setX(targetPos.x() + length)
            targetPos.setY(targetPos.y() + length)
        elif direction == Direction.UpRight:
            targetPos.setX(targetPos.x() + length)
            targetPos.setY(targetPos.y() - length)

        return targetPos
