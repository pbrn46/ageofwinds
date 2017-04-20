#!/usr/bin/env python

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from game import Game
from gameModel import GameModel
from gameView import GameView
from gameControl import GameControl


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    model = GameModel(game)
    view = GameView(game)
    control = GameControl(game)
    game.set_model(model)
    game.set_view(view)
    game.set_control(control)
    view.generate_view()
    app.exec_()
