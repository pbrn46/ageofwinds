from PySide.QtGui import *


class EquipmentSection(QWidget):
    def __init__(self, parent=None):
        super(EquipmentSection, self).__init__(parent)
        self.layout1 = QVBoxLayout()
        self.setLayout(self.layout1)

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

        self.layout2.addWidget(QLabel("Armor"), 0, 0)
        self.layout2.addWidget(QLabel("Neckwear"), 0, 1)
        self.layout2.addWidget(QLabel("Overgarment"), 0, 2)
        self.layout2.addWidget(QLabel("Helmet"), 0, 3)
        self.layout2.addWidget(QLabel("Shield"), 0, 4)

        self.layout2.addWidget(QLabel("Bracers"), 1, 0)
        self.layout2.addWidget(QLabel("Gauntlet"), 1, 4)

        self.layout2.addWidget(QLabel("Weapon"), 2, 0)
        self.layout2.addWidget(QLabel("FreeHand"), 2, 4)

        self.layout2.addWidget(QLabel("Right Ring"), 3, 0)
        self.layout2.addWidget(QLabel("Left Right"), 3, 4)

        self.layout2.addWidget(QLabel("Belt"), 4, 0)
        self.layout2.addWidget(QLabel("Boots"), 4, 4)

        self.layout2.addWidget(QLabel("Bag"), 5, 0)
        self.layout2.addWidget(QLabel("Purse"), 5, 4)


