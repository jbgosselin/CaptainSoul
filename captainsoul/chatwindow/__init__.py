# -*- coding: utf-8 -*-

import gtk

from captainsoul.common import CptCommon, ignoreParams
from captainsoul.chatwindow.chatview import ChatView
from captainsoul.chatwindow.chatstatus import ChatStatus
from captainsoul.chatwindow.chatentry import ChatEntry


class ChatWindow(gtk.Window, CptCommon):
    def __init__(self, login, iconify, msg=None):
        super(ChatWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul - %s" % login
        )
        self.resize(self.config['chatWidth'], self.config['chatHeight'])
        self._createUi(login, msg)
        self.connect("delete-event", self.manager.closeChatWindowEvent, login)
        self.connect("configure-event", self.resizeEvent)
        if iconify:
            self.iconify()
        self.show_all()

    def _createUi(self, login, msg):
        box = gtk.VBox(False, 0)
        self.add(box)
        # chatview
        box.add(ChatView(login, msg))
        # is typing bar
        box.pack_start(ChatStatus(login), False, False, 0)
        # user entry
        entry = ChatEntry(login)
        self.connect('delete-event', entry.deleteEvent, login)
        box.pack_start(entry, False, False, 0)

    @ignoreParams
    def resizeEvent(self):
        self.config['chatWidth'], self.config['chatHeight'] = self.get_size()
