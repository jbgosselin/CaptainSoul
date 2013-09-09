# -*- coding: utf-8 -*-

import gtk

from cptsoul.common import CptCommon


class ChatStatus(gtk.Statusbar, CptCommon):
    def __init__(self, login):
        super(ChatStatus, self).__init__()
        self.connect('destroy', self.destroyEvent)
        self._connections = [
            self.manager.connect('is-typing', self.isTypingEvent, login),
            self.manager.connect('cancel-typing', self.cancelTypingEvent, login)
        ]

    def isTypingEvent(self, widget, info, login):
        if info.login == login:
            self.push(0, "Is typing...")

    def cancelTypingEvent(self, widget, info, login):
        if info.login == login:
            self.remove_all(0)

    def destroyEvent(self, widget):
        for co in self._connections:
            self.manager.disconnect(co)
