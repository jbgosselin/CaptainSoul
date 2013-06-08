# -*- coding: utf-8 -*-

import gtk

from .. import Icons
from ChatView import ChatView
from ChatStatus import ChatStatus


class ChatWindow(gtk.Window):
    def __init__(self, manager, login, iconify):
        super(ChatWindow, self).__init__()
        self.set_properties(title="CaptainSoul - %s" % login, icon=Icons.shield.get_pixbuf())
        self._typing = False
        self._createUi(manager, login)
        self.connect("delete-event", self.deleteEvent, manager, login)
        self.connect("delete-event", manager.closeChatWindowEvent, login)
        self.resize(200, 200)
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
        view = gtk.TextView()
        view.set_properties(editable=True, cursor_visible=True, wrap_mode=gtk.WRAP_WORD_CHAR)
        self._entry = view.get_buffer()
        view.set_size_request(100, 30)
        view.connect("key-press-event", self.keyPressEvent, manager, login)
        self._entry.connect("changed", self.keyPressEventEnd, manager, login)
        box.pack_start(view, False, False, 0)

    def deleteEvent(self, widget, reason, manager, login):
        if self._typing:
            self._typing = False
            manager.sendCancelTyping([login])

    def keyPressEvent(self, widget, event, manager, login):
        if gtk.gdk.keyval_name(event.keyval) in ('Return', 'KP_Enter'):
            text = self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True)
            if len(text):
                self._entry.delete(self._entry.get_start_iter(), self._entry.get_end_iter())
                manager.sendMsg(text, [login])
            return True

    def keyPressEventEnd(self, widget, manager, login):
        l = len(self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True))
        if not self._typing and l >= 5:
            manager.sendStartTyping([login])
            self._typing = True
        elif self._typing and l < 5:
            manager.sendCancelTyping([login])
            self._typing = False
