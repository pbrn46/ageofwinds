#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *


class MainToolbar(QToolBar):
    def __init__(self, game, parent=None):
        super(MainToolbar, self).__init__(parent)
        self.game = game

        self.setFocusPolicy(Qt.NoFocus)

        self.actionButtons = []
        self.spellButtons = []

        self.actionTexts = ['Get',
                            'Free Hand',
                            'Search',
                            'Disarm',
                            'Rest',
                            'Save']

        self.build_action_buttons()

        self.addSeparator()

        self.build_spell_buttons()

    def build_action_buttons(self):
        for text in self.actionTexts:
            button = QToolButton(self)
            button.setFocusPolicy(Qt.NoFocus)
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            button.setText(text)
            self.actionButtons.append(button)
            self.addWidget(button)
            button.setAutoRaise(False)  # Have to be set after adding to QToolBar

    def build_spell_buttons(self):
        for i in range(20):
            button = QToolButton(self)
            button.setFocusPolicy(Qt.NoFocus)
            self.actionButtons.append(button)
            self.addWidget(button)
            spell = None
            spell_name = ""
            try:
                spell = self.game.model.spellList[i]
                spell_name = spell.get_name()
                button.setToolTip(spell_name)
                icon = spell.get_attribute("icon")
                if icon:
                    icon = int(icon)
                    # TODO: Change from spritePix to spellIconPix or something
                    button.setIcon(self.game.view.spritePix[icon])
            except IndexError:
                pass
            button.setAutoRaise(False)  # Have to be set after adding to QToolBar
            button.pressed.connect(lambda i=i: self.spell_button_action(i))

    def spell_button_action(self, button_id):
        self.game.model.spellList.cast(button_id)
