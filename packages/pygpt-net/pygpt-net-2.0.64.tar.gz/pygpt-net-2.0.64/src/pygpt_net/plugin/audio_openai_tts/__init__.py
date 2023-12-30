#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.28 21:00:00                  #
# ================================================== #

import os

from PySide6.QtCore import Slot
from openai import OpenAI

from pygpt_net.plugin.base import BasePlugin

from .worker import Worker


class Plugin(BasePlugin):
    def __init__(self):
        super(Plugin, self).__init__()
        self.id = "audio_openai_tts"
        self.name = "Audio Output (OpenAI TTS)"
        self.type = ['audio.output']
        self.description = "Enables audio/voice output (speech synthesis) using OpenAI TTS (Text-To-Speech) API"
        self.allowed_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        self.allowed_models = ['tts-1', 'tts-1-hd']
        self.input_text = None
        self.window = None
        self.playback = None
        self.order = 1
        self.use_locale = True
        self.init_options()

    def init_options(self):
        """
        Initialize options
        """
        self.add_option("model", "text", "tts-1",
                        "Model",
                        "Specify model, available models: tts-1, tts-1-hd")
        self.add_option("voice", "text", "alloy",
                        "Voice",
                        "Specify voice, available voices: alloy, echo, fable, onyx, nova, shimmer")

    def setup(self):
        """
        Return available config options

        :return: config options
        """
        return self.options

    def setup_ui(self):
        """
        Setup UI
        """
        pass

    def attach(self, window):
        """
        Attach window

        :param window: Window instance
        """
        self.window = window

    def handle(self, event, *args, **kwargs):
        """
        Handle dispatched event

        :param event: event object
        """
        name = event.name
        data = event.data
        ctx = event.ctx

        if name == 'input.before':
            self.on_input_before(data['value'])
        elif name == 'ctx.after':
            self.on_ctx_after(ctx)
        elif name == 'audio.read_text':
            self.on_ctx_after(ctx)
        elif name == 'audio.output.stop':
            self.stop_audio()

    def on_input_before(self, text):
        """
        Event: Before input

        :param text: text
        """
        self.input_text = text

    def on_ctx_after(self, ctx):
        """
        Event: After ctx

        :param ctx: CtxItem
        """
        text = ctx.output
        try:
            if text is not None and len(text) > 0:
                client = OpenAI(
                    api_key=self.window.core.config.get('api_key'),
                    organization=self.window.core.config.get('organization_key'),
                )
                voice = self.get_option_value('voice')
                model = self.get_option_value('model')
                path = os.path.join(self.window.core.config.path, 'output.mp3')

                if model not in self.allowed_models:
                    model = 'tts-1'
                if voice not in self.allowed_voices:
                    voice = 'alloy'

                # worker
                worker = Worker()
                worker.plugin = self
                worker.client = client
                worker.model = model
                worker.path = path
                worker.voice = voice
                worker.text = text

                # signals
                worker.signals.playback.connect(self.handle_playback)
                worker.signals.stop.connect(self.handle_stop)
                worker.signals.status.connect(self.handle_status)
                worker.signals.error.connect(self.handle_error)

                # start
                self.window.threadpool.start(worker)

        except Exception as e:
            self.window.core.debug.log(e)

    def destroy(self):
        """
        Destroy thread
        """
        pass

    def set_status(self, status):
        """
        Set status

        :param status:status
        """
        self.window.ui.plugin_addon['audio.output'].set_status(status)

    def show_stop_button(self):
        """
        Show stop button
        """
        self.window.ui.plugin_addon['audio.output'].stop.setVisible(True)

    def hide_stop_button(self):
        """
        Hide stop button
        """
        self.window.ui.plugin_addon['audio.output'].stop.setVisible(False)

    def stop_speak(self):
        """
        Stop speaking
        """
        self.window.ui.plugin_addon['audio.output'].stop.setVisible(False)
        self.window.ui.plugin_addon['audio.output'].set_status('Stopped')
        self.window.ui.plugin_addon['audio.output'].stop_audio()

    def stop_audio(self):
        """
        Stop playing the audio
        """
        if self.playback is not None:
            self.playback.stop()
            self.playback = None

    @Slot(object)
    def handle_status(self, data):
        """
        Handle thread status msg
        :param data
        """
        self.set_status(str(data))

    @Slot(object)
    def handle_error(self, error):
        """
        Handle thread error
        :param error
        """
        self.window.core.debug.log(error)

    @Slot(object)
    def handle_playback(self, playback):
        """
        Handle thread playback object
        :param playback
        """
        self.playback = playback

    @Slot()
    def handle_stop(self):
        """
        Handle thread playback stop
        """
        self.stop_audio()
