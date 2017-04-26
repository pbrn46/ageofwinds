from PySide.QtGui import *
from PySide.QtCore import Qt


class EquipmentSectionSlot(QFrame):
    def __init__(self, game, slot_name, parent=None):
        super(EquipmentSectionSlot, self).__init__(parent)
        self.game = game
        self.slot_name = slot_name

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.label = QLabel(slot_name)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
