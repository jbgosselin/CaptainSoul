# -*- coding: utf-8 -*-

import gtk

from ..Config import Config
from .. import Icons
from ChatView import ChatView
from ChatStatus import ChatStatus
from ChatEntry import ChatEntry


class ChatWindow(gtk.Window):
    def __init__(self, manager, login, iconify):
        super(ChatWindow, self).__init__()
        self.set_properties(title="CaptainSoul - %s" % login, icon=Icons.shield.get_pixbuf())
        self._typing = False
        self._createUi(manager, login)
        self.resize(Config['chatWidth'], Config['chatHeight'])
        self.connect("delete-event", manager.closeChatWindowEvent, login)
        self.connect("configure-event", self.resizeEvent)
        if iconify:
            self.iconify()
        self.show_all()

    def _createUi(self, manager, login):
        box = gtk.VBox(False, 0)
        self.add(box)
        # chatview
        box.add(ChatView(manager, login))
        # is typing bar
        box.pack_start(ChatStatus(manager, login), False, False, 0)
        # user entry
        entry = ChatEntry(manager, login)
        self.connect('delete-event', entry.deleteEvent, manager, login)
        box.pack_start(entry, False, False, 0)

    def resizeEvent(self, *args, **kwargs):
        Config['chatWidth'], Config['chatHeight'] = self.get_size()
