from PySide.QtGui import *
from PySide.QtCore import *


class InventoryMdiSubWindow(QMdiSubWindow):
    def __init__(self, game, parent=None):
        super(InventoryMdiSubWindow, self).__init__(parent)
        self.game = game
        self.fixedPos = QPoint(0, 0)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def mouseMoveEvent(self, event):
        super(InventoryMdiSubWindow, self).mouseMoveEvent(event)
        if self.pos() != self.fixedPos:
            self.move(self.fixedPos)

    def setFixedPos(self, pos):
        self.fixedPos = QPoint(pos)
        self.move(self.fixedPos)

    def closeEvent(self, event):
        super(InventoryMdiSubWindow, self).closeEvent(event)
        self.setVisible(False)
        self.game.view.mainWindow.screens["inventory"].inventory.tileSubWindowsVertical()

    # def resize(self, *args, **kwargs):
    #     return False
