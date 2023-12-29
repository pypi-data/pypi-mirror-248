#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.26 21:00:00                  #
# ================================================== #

import webbrowser

from .editor import Editor
from .files import Files
from .threads import Threads

from pygpt_net.utils import trans


class Assistant:
    def __init__(self, window=None):
        """
        Assistants controller

        :param window: Window instance
        """
        self.window = window
        self.editor = Editor(window)
        self.files = Files(window)
        self.threads = Threads(window)

    def setup(self):
        """Setup assistants"""
        self.window.core.assistants.load()
        self.update()

    def update(self, update_list=True):
        """
        Update assistants list

        :param update_list: update list
        """
        if update_list:
            self.update_list()
        self.window.controller.assistant.files.update_list()
        self.select_current()

    def update_list(self):
        """Update assistants list"""
        items = self.window.core.assistants.get_all()
        self.window.ui.toolbox.assistants.update(items)

    def refresh(self):
        """Update assistants"""
        self.select_default()

    def select(self, idx):
        """
        Select assistant on the list

        :param idx: idx on the list
        """
        # check if change is not locked
        if self.change_locked():
            return

        # mark assistant as selected
        id = self.window.core.assistants.get_by_idx(idx)
        self.select_by_id(id)

    def select_by_id(self, id):
        """
        Select assistant on the list

        :param id: assistant ID
        """
        self.window.core.config.set('assistant', id)

        # update attachments list with list of attachments from assistant
        mode = self.window.core.config.get('mode')
        assistant = self.window.core.assistants.get_by_id(id)
        self.window.controller.attachment.import_from_assistant(mode, assistant)
        self.window.controller.attachment.update()
        self.update(False)

        # update model if exists in assistant
        if assistant is not None:
            model = assistant.model
            if model is not None and model != "":
                if model in self.window.core.models.items:
                    self.window.core.config.set('model', model)
                    self.window.core.config.data['current_model'][mode] = model
                    self.refresh()

        self.window.controller.ctx.update_ctx()  # update current ctx info

    def select_current(self):
        """Select assistant by current"""
        assistant_id = self.window.core.config.get('assistant')
        items = self.window.core.assistants.get_all()
        if assistant_id in items:
            idx = list(items.keys()).index(assistant_id)
            current = self.window.ui.models['assistants'].index(idx, 0)
            self.window.ui.nodes['assistants'].setCurrentIndex(current)

    def select_default(self):
        """Set default assistant"""
        assistant = self.window.core.config.get('assistant')
        if assistant is None or assistant == "":
            mode = self.window.core.config.get('mode')
            if mode == 'assistant':
                self.window.core.config.set('assistant', self.window.core.assistants.get_default_assistant())
                self.update()

    def create(self):
        """Create assistant"""
        assistant = self.window.core.assistants.create()
        self.editor.assign_data(assistant)
        try:
            return self.window.core.gpt.assistants.create(assistant)
        except Exception as e:
            self.window.core.debug.log(e)
            self.window.ui.dialogs.alert(str(e))

    def update_data(self, assistant):
        """Update assistant"""
        self.editor.assign_data(assistant)
        try:
            return self.window.core.gpt.assistants.update(assistant)
        except Exception as e:
            self.window.core.debug.log(e)
            self.window.ui.dialogs.alert(str(e))

    def import_api(self, force=False):
        """
        Import all remote assistants from API

        :param force: if true, imports without confirmation
        """
        if not force:
            self.window.ui.dialogs.confirm('assistant_import', '',
                                           trans('confirm.assistant.import'))
            return

        try:
            # import assistants
            items = self.window.core.assistants.get_all()
            self.window.core.gpt.assistants.import_api(items)
            self.window.core.assistants.items = items
            self.window.core.assistants.save()

            # import uploaded files
            for id in self.window.core.assistants.items:
                assistant = self.window.core.assistants.get_by_id(id)
                self.window.controller.assistant.files.import_files(assistant)
            # status
            self.window.set_status("Imported assistants: " + str(len(items)))
        except Exception as e:
            self.window.core.debug.log(e)
            print("Error importing assistants")
            self.window.ui.dialogs.alert(str(e))
        self.update()

    def clear(self, force=False):
        """
        Clear assistant data

        :param force: force clear data
        """
        id = self.window.core.config.get('assistant')

        if not force:
            self.window.ui.dialogs.confirm('assistant_clear', '',
                                           trans('confirm.assistant.clear'))
            return

        if id is not None and id != "":
            if self.window.core.assistants.has(id):
                assistant = self.window.core.assistants.get_by_id(id)
                assistant.reset()

        self.window.set_status(trans('status.assistant.cleared'))
        self.update()

    def delete(self, idx=None, force=False):
        """
        Delete assistant

        :param idx: assistant index (row index)
        :param force: force delete without confirmation
        """
        if idx is not None:
            id = self.window.core.assistants.get_by_idx(idx)
            if id is not None and id != "":
                if self.window.core.assistants.has(id):
                    # if exists then show confirmation dialog
                    if not force:
                        self.window.ui.dialogs.confirm('assistant_delete', idx,
                                                       trans('confirm.assistant.delete'))
                        return

                    # clear if this is current assistant
                    if id == self.window.core.config.get('assistant'):
                        self.window.core.config.set('assistant', None)
                        self.window.core.config.set('assistant_thread', None)

                    # delete in API
                    try:
                        self.window.core.gpt.assistants.delete(id)
                    except Exception as e:
                        self.window.ui.dialogs.alert(str(e))

                    self.window.core.assistants.delete(id)
                    self.update()
                    self.window.set_status(trans('status.assistant.deleted'))

    def goto_online(self):
        """Open Assistants page"""
        webbrowser.open('https://platform.openai.com/assistants')

    def change_locked(self):
        """
        Check if assistant change is locked

        :return: true if locked
        :rtype: bool
        """
        if self.window.controller.input.generating:
            return True
        return False
