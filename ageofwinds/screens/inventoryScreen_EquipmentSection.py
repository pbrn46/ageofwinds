from PySide.QtGui import *
from screens.inventoryScreen_EquipmentSectionSlot import EquipmentSectionSlot


class EquipmentSection(QWidget):
    def __init__(self, game, parent=None):
        super(EquipmentSection, self).__init__(parent)
        self.game = game
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setSpacing(0)

        # self.title = QLabel("Armor")
        # self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.layout1.addWidget(self.title)

        """
        Armor Neckwear Overgarment Helmet Shield
        Bracers Gauntlets
        Weapon FreeHand
        RightRing LeftRing
        Belt Boots
        Bag Purse
        """
        self.layout2 = QGridLayout()
        self.layout1.addLayout(self.layout2)
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout2.setSpacing(0)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "armor"), 0, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "neckwear"), 0, 1)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "overgarment"), 0, 2)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "helmet"), 0, 3)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "shield"), 0, 4)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "bracers"), 1, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "gauntlet"), 1, 4)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "weapon"), 2, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "freeHand"), 2, 4)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "right_ring"), 3, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "left_right"), 3, 4)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "belt"), 4, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "boots"), 4, 4)

        self.layout2.addWidget(EquipmentSectionSlot(self.game, "bag"), 5, 0)
        self.layout2.addWidget(EquipmentSectionSlot(self.game, "purse"), 5, 4)


