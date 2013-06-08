# -*- coding: utf-8 -*-

import gtk


class ChatStatus(gtk.Statusbar):
    def __init__(self, manager, login):
        super(ChatStatus, self).__init__()
        manager.connect('is-typing', self.isTypingEvent, login)
        manager.connect('cancel-typing', self.cancelTypingEvent, login)

    def isTypingEvent(self, widget, info, login):
        if info.login == login:
            self.push(0, "Is typing...")

    def cancelTypingEvent(self, widget, info, login):
        if info.login == login:
            self.remove_all(0)
