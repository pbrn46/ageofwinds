
from PySide.QtGui import *


class Screen(QWidget):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent)

    def toggled(self, visible_state):
        """Slot. To be called after screen is toggled to be visible or not
         
         Keyword arguments:
             visible_state -- True if shown, False if hidden"""
        pass
