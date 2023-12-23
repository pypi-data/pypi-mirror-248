#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.22 02:00:00                  #
# ================================================== #

from ..updater import Updater


class Launcher:
    def __init__(self, window=None):
        """
        Launcher controller

        :param window: Window instance
        """
        self.window = window
        self.updater = Updater(window)

    def migrate_version(self):
        """Patch config files if needed"""
        self.updater.patch()

    def show_api_monit(self):
        """Show empty API KEY monit"""
        self.window.ui.dialogs.open('info.start')

    def check_updates(self):
        """Check for updates"""
        self.updater.check(True)

    def setup(self):
        """Setup launcher"""
        self.updater.check()

        # show welcome API KEY dialog
        if self.window.config.get('api_key') is None or self.window.config.get('api_key') == '':
            self.show_api_monit()

        self.window.app.gpt.init()
        self.window.app.images.init()
        self.window.controller.settings.update_font_size()
