from PySide.QtGui import *
from PySide.QtCore import *

from ageofwinds.screens.inventoryScreen_InventoryMdiSubWindow import InventoryMdiSubWindow


class InventoryMdi(QMdiArea):
    def __init__(self, game, parent=None):
        super(InventoryMdi, self).__init__(parent)
        self.game = game
        self.floor_window = InventoryMdiSubWindow(game)
        self.floor_window.setWindowTitle("Floor")
        self.addSubWindow(self.floor_window)

        self.bag_windows = []
        self.create_bag_window(0)
        self.tileSubWindowsVertical()

    def resizeEvent(self, event):
        super(InventoryMdi, self).resizeEvent(event)
        self.tileSubWindowsVertical()

    def create_bag_window(self, bag_id):
        """Create a bag window."""
        # TODO: Pull a bag ID from database?
        window = InventoryMdiSubWindow(self.game)
        window.setWindowTitle("Bag001")

        self.bag_windows.append(window)
        self.addSubWindow(window)

    def show_bag_window(self, bag_index):
        self.bag_windows[bag_index].setVisible(True)

    def hide_bag_window(self, bag_index):
        self.bag_windows[bag_index].setVisible(False)

    def tileSubWindowsVertical(self):
        visible_windows = self.visibleSubWindowList()
        pos = QPoint(0, 0)
        for w in visible_windows:
            size = QSize(self.width(), self.height() / len(visible_windows))
            rect = QRect(0, 0, size.width(), size.height())

            w.setGeometry(rect)
            # w.setFixedSize(size)
            w.move(pos)
            w.setFixedPos(pos)
            pos.setY(pos.y() + w.height())

    def visibleSubWindowList(self):
        l = []
        for w in self.subWindowList():
            if w.isVisible():
                l.append(w)
        return l
