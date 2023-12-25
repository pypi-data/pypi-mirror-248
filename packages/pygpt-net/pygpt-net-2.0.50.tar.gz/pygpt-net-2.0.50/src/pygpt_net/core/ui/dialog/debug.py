#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.22 18:00:00                  #
# ================================================== #

from PySide6.QtWidgets import QTreeView, QGridLayout, QAbstractItemView, QScrollArea

from ..widget.dialog.debug import DebugDialog


class Debug:
    def __init__(self, window=None):
        """
        Debug setup

        :param window: Window instance
        """
        self.window = window

    def setup(self, id):
        """
        Setup debug dialog

        :param id: debug id
        """
        self.window.ui.debug[id] = QTreeView()
        self.window.ui.debug[id].setRootIsDecorated(False)
        self.window.ui.debug[id].setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.window.ui.debug[id].setWordWrap(True)

        scroll = QScrollArea()
        scroll.setWidget(self.window.ui.debug[id])
        scroll.setWidgetResizable(True)

        layout = QGridLayout()
        layout.addWidget(scroll, 1, 0)

        self.window.ui.dialog['debug.' + id] = DebugDialog(self.window, id)
        self.window.ui.dialog['debug.' + id].setLayout(layout)
        self.window.ui.dialog['debug.' + id].setWindowTitle("Debug" + ": " + id)
