#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.05 22:00:00                  #
# ================================================== #
import os


class AssistantsDebug:
    def __init__(self, window=None):
        """
        Assistants debug

        :param window: Window instance
        """
        self.window = window
        self.id = 'assistants'

    def update(self):
        """Update debug window."""
        self.window.app.debug.begin(self.id)

        path = os.path.join(self.window.config.path, '', self.window.app.assistants.config_file)
        self.window.app.debug.add(self.id, 'File', path)

        # assistants
        assistants = self.window.app.assistants.get_all()
        for key in assistants:
            prefix = "[{}] ".format(key)
            assistant = assistants[key]
            self.window.app.debug.add(self.id, prefix + 'ID', str(key))
            self.window.app.debug.add(self.id, 'id', str(assistant.id))
            self.window.app.debug.add(self.id, 'name', str(assistant.name))
            self.window.app.debug.add(self.id, 'description', str(assistant.description))
            self.window.app.debug.add(self.id, 'model', str(assistant.model))
            self.window.app.debug.add(self.id, 'instructions', str(assistant.instructions))
            self.window.app.debug.add(self.id, 'meta', str(assistant.meta))
            self.window.app.debug.add(self.id, 'tools', str(assistant.tools))
            self.window.app.debug.add(self.id, 'files', str(assistant.files))

        self.window.app.debug.end(self.id)
