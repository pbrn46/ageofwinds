#!/usr/bin/env python

from PySide.QtGui import *

from ageofwinds.screens.screens import Screens
from mainMenu import MainMenu
from mainToolbar import MainToolbar
from statusWindow import StatusWindow


class MainWindow(QMainWindow):
    def __init__(self, game, parent=None):
        super(MainWindow, self).__init__(parent)
        self.game = game

        # self.mdi = QMdiArea()
        # self.centralWidget = self.mdi

        self.setWindowTitle("Age of Winds")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.centralWidget.setLayout(self.layout)

        self.screens = Screens(self.game)
        self.layout.addWidget(self.screens)

        self.build_menu()

        self.toolbar = MainToolbar(self.game)
        self.addToolBar(self.toolbar)

        self.statusWindow = StatusWindow(self.game)
        self.layout.addWidget(self.statusWindow)

        self.build_status_bar()

        self.show()

    def build_menu(self):
        menu_bar = MainMenu(self.game)
        self.setMenuBar(menu_bar)

    def build_status_bar(self):
        status_bar = self.statusBar()
