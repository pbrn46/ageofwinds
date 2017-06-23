from PySide.QtGui import *
from PySide.QtCore import *

from screens.inventoryScreen_InventoryMdiBagWindow import InventoryMdiBagWindow


class InventoryMdi(QMdiArea):
    def __init__(self, game, parent=None):
        super(InventoryMdi, self).__init__(parent)
        self.game = game
        self.floor_window = InventoryMdiBagWindow(self.game, -1)
        self.floor_window.setWindowTitle("Floor")
        self.addSubWindow(self.floor_window)

        self.bag_windows = []
        self.create_bag_window(0)
        self.tileSubWindows()

    def resizeEvent(self, event):
        # super(InventoryMdi, self).resizeEvent(event)
        self.tileSubWindows()

    def create_bag_window(self, inventory_id):
        """Create a bag window."""
        # TODO: Pull a bag ID from database?

        if self.get_bag_window(inventory_id) is None:
            window = InventoryMdiBagWindow(self.game, inventory_id)
            window.setWindowTitle("Bag001")
            self.bag_windows.append(window)
            self.addSubWindow(window)
            return True
        else:
            return False

    def show_bag_window(self, bag_index):
        self.bag_windows[bag_index].setVisible(True)

    def hide_bag_window(self, bag_index):
        self.bag_windows[bag_index].setVisible(False)

    def refresh_bags(self):
        for w in self.bag_windows:
            w.refresh_item_widgets()

    def tileSubWindows(self, orientation=Qt.Vertical):
        """Tile subwindows.
        
        Keyword Arguments:
            orientation -- Qt.Orientations flag, either Qt.Vertical or Qt.Horizontal
        """
        if orientation == Qt.Vertical:
            visible_windows = self.visible_sub_window_list()
            pos = QPoint(0, 0)
            for w in visible_windows:
                size = QSize(self.width(), self.height() / len(visible_windows))
                rect = QRect(0, 0, size.width(), size.height())

                w.setGeometry(rect)
                # w.setFixedSize(size)
                w.move(pos)
                w.setFixedPos(pos)
                pos.setY(pos.y() + w.height())
        elif orientation == Qt.Horizontal:
            super(InventoryMdi, self).tileSubWindows()

    def visible_sub_window_list(self):
        l = []
        for w in self.subWindowList():
            if w.isVisible():
                l.append(w)
        return l

    def get_bag_window(self, inventory_id):
        for w in self.subWindowList():
            if w.inventory_id == inventory_id:
                return w
        return None
