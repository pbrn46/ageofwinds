#!/usr/bin/env python

import sys
import os
from PySide.QtGui import *
from game import Game
from gameModel import GameModel
from gameView import GameView
from gameControl import GameControl

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def run_main():
    app = QApplication(sys.argv)
    game = Game()
    model = GameModel(game)
    view = GameView(game)
    control = GameControl(game)
    game.set_model(model)
    game.set_view(view)
    game.set_control(control)
    game.control.init_game()
    game.control.begin_test_mode()  # TODO: Debug
    app.exec_()

if __name__ == '__main__':
    run_main()
