#!/usr/bin/env python


from PySide.QtCore import *
from PySide.QtGui import *


class Game:
    def __init__(self):
        self.model = None
        self.view = None
        self.control = None

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def set_control(self, control):
        self.control = control
