from PySide.QtGui import *
from PySide.QtCore import *


class InventoryMdiBagWindow(QMdiSubWindow):
    def __init__(self, game, inventory_id, parent=None):
        super(InventoryMdiBagWindow, self).__init__(parent)
        self.game = game
        self.inventory_id = inventory_id
        self.fixedPos = QPoint(0, 0)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.list_widget = QListWidget()
        self.setWidget(self.list_widget)
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setMovement(QListWidget.Static)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setGridSize(QSize(72, 72))
        self.list_widget.setResizeMode(QListWidget.Adjust)

        self.item_widgets = []

        if self.inventory_id == 0:  # TODO: Debug
            self.game.model.inventory.load_sample_data()
        self.refresh_item_widgets()

    def mouseMoveEvent(self, event):
        super(InventoryMdiBagWindow, self).mouseMoveEvent(event)
        if self.pos() != self.fixedPos:
            self.move(self.fixedPos)

    def setFixedPos(self, pos):
        self.fixedPos = QPoint(pos)
        self.move(self.fixedPos)

    def closeEvent(self, event):
        super(InventoryMdiBagWindow, self).closeEvent(event)
        self.setVisible(False)
        self.game.view.mainWindow.screens["inventory"].inventory.tileSubWindows()

    def refresh_item_widgets(self):
        self.item_widgets = []
        for item in self.game.model.inventory:
            if item.parent == self.inventory_id:
                self.item_widgets.append(item)

        self.list_widget.clear()
        for item in self.item_widgets:
            widget_item = QListWidgetItem()
            widget_item.setText(item.name)
            widget_item.setIcon(item.icon)
            self.list_widget.addItem(widget_item)
