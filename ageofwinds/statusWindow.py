#!/usr/bin/env python

from PySide.QtCore import *
from PySide.QtGui import *

from collections import OrderedDict


class StatusWindow(QWidget):
    def __init__(self, game, parent=None):
        super(StatusWindow, self).__init__(parent)
        self.game = game
        self.logList = None
        self.statsList = None

        self.statsItems = OrderedDict()

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.vLayout = QVBoxLayout()
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(0)
        self.setLayout(self.vLayout)  #

        self.hLayout = QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)
        self.vLayout.addLayout(self.hLayout)  #

        self.build_log_list()
        self.build_stats_list()

    def build_log_list(self):
        self.logList = QListWidget()
        self.logList.setFocusPolicy(Qt.NoFocus)
        self.hLayout.addWidget(self.logList)

        self.logList.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        self.game.model.logList = self.logList

    def build_stats_list(self):
        self.statsList = QListWidget()
        self.statsList.setFocusPolicy(Qt.NoFocus)
        self.hLayout.addWidget(self.statsList)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

        self.statsItems["hp"] = QListWidgetItem("HP 0 (0)")
        self.statsItems["mp"] = QListWidgetItem("MP 100 (100)")
        self.statsItems["lvl"] = QListWidgetItem("Level 1 (Exp 0/100)")
        self.statsItems["time"] = QListWidgetItem("Time")
        self.statsItems["loc"] = QListWidgetItem("Location")

        for key, item in self.statsItems.items():
            # item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.statsList.addItem(item)
        # self.statsList.setStyleSheet("QListWidget::item:disabled {background: transparent;}")
        self.statsList.setStyleSheet("QListWidget::item {background: transparent;}")

        self.game.model.statsUpdateEvent = self.update_stats

        self.statsList.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # self.setFixedHeight()
        self.update_stats_list_width()

        self.update_stats()

    def update_stats_list_width(self):
        stats_list_height = 0
        for i in range(self.statsList.count()):
            stats_list_height += self.statsList.sizeHintForRow(i)
        stats_list_height += 2 * self.statsList.frameWidth()
        self.statsList.setMinimumWidth(self.statsList.sizeHintForColumn(0))
        self.statsList.setFixedHeight(stats_list_height)
        self.statsList.setFixedWidth(self.statsList.sizeHintForColumn(0) + 2 * self.statsList.frameWidth())

    def update_stats(self):
        stats = self.game.model.protagonist.stats

        self.statsItems["hp"].setText("HP %s (%s)" % (stats["current_hp"], stats["max_hp"]))
        self.statsItems["mp"].setText("MP %s (%s)" % (stats["current_mp"], stats["max_mp"]))
        # self.statsItems["lvl"] = QListWidgetItem("Level 1 (0/10)")
        self.statsItems["time"].setText("Time %s" % (self.game.model.gameTime.get_time_string()))
        # self.statsItems["loc"] = QListWidgetItem("Location")

        self.check_stats()

        self.update_stats_list_width()

    def check_stats(self):
        stats = self.game.model.protagonist.stats

        if stats["current_hp"] == 0 or stats["current_hp"] / stats["max_hp"] < 0.25:
            self.set_item_critical(self.statsItems["hp"])
        else:
            self.set_item_non_critical(self.statsItems["hp"])

        if stats["current_mp"] == 0 or stats["current_mp"] / stats["max_mp"] < 0.25:
            self.set_item_critical(self.statsItems["mp"])
        else:
            self.set_item_non_critical(self.statsItems["mp"])

    def set_item_critical(self, item):
        item.setForeground(Qt.red)
        f = QFont()
        f.setBold(True)
        item.setFont(f)

    def set_item_non_critical(self, item):
        item.setForeground(Qt.black)
        f = QFont()
        f.setBold(False)
        item.setFont(f)

