#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.23 01:00:00                  #
# ================================================== #

from PySide6.QtWidgets import QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout

from ..widget.dialog.logger import LoggerDialog
from ...utils import trans


class Logger:
    def __init__(self, window=None):
        """
        Logger dialog

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup logger dialog"""
        self.window.logger = QPlainTextEdit()
        self.window.logger.setReadOnly(True)

        self.window.ui.nodes['logger.btn.clear'] = QPushButton(trans("dialog.logger.btn.clear"))
        self.window.ui.nodes['logger.btn.clear'].clicked.connect(
            lambda: self.window.controller.debug.logger_clear())

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.window.ui.nodes['logger.btn.clear'])

        layout = QVBoxLayout()
        layout.addWidget(self.window.logger)
        layout.addLayout(bottom_layout)

        self.window.ui.dialog['logger'] = LoggerDialog(self.window)
        self.window.ui.dialog['logger'].setLayout(layout)
        self.window.ui.dialog['logger'].setWindowTitle(trans('dialog.logger.title'))
