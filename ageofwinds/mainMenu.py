#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *


class MainMenu(QMenuBar):
    def __init__(self, game):
        super(MainMenu,self).__init__()
        self.game = game
        self.fileMenu = self.addMenu('&File')
        self.fileMenu.setStatusTip('File menu')
        self.exitAction = QAction(QIcon('exit.png'), 'E&xit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.action_quit)
        self.fileMenu.addAction(self.exitAction)

        self.inventoryAction = QAction('&Inventory', self)
        # inventoryAction.setShortcut('Ctrl+Q')
        self.inventoryAction.setStatusTip('Inventory')
        # inventoryAction.triggered.connect(self.close)
        self.addAction(self.inventoryAction)

        self.characterAction = QAction('&Character', self)
        # characterAction.setShortcut('Ctrl+Q')
        self.characterAction.setStatusTip('Character')
        # characterAction.triggered.connect(self.close)
        self.addAction(self.characterAction)

        self.spellMenu = self.addMenu('&Spells')
        self.spellMenu.setStatusTip('Spell menu')
        self.build_spell_menu()

    def action_quit(self):
        self.game.control.quit()

    def build_spell_menu(self):
        for i in range(10):
            shortcut = i + 1
            if shortcut == 10:
                shortcut = 0

            spell = None
            spell_name = "None"
            action = QAction(self.spellMenu)
            action.setShortcut("Ctrl+%s" % (shortcut))
            try:
                spell = self.game.model.spellList[i]
                spell_name = spell.get_name()
                action.triggered.connect(lambda i=i, action=action: self.action_spell_cast(action, i))
                icon = spell.get_attribute("icon")
                if icon:
                    icon = int(icon)
                    # TODO: Change from spritePix to spellIconPix or something
                    action.setIcon(self.game.view.spritePix[icon])
            except IndexError:
                pass

            action.setText("&%s: %s" % (shortcut, spell_name))

            self.spellMenu.addAction(action)

    def action_spell_cast(self, action, index):
        self.game.model.spellList.cast(index)


