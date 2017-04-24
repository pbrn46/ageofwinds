from PySide.QtGui import *


class InventoryMdi(QMdiArea):
    def __init__(self, parent=None):
        super(InventoryMdi, self).__init__(parent)
        self.floor_window = QMdiSubWindow()
        self.floor_window.setWindowTitle("Floor")
        # self.floor_window.resize()
        self.addSubWindow(self.floor_window)
