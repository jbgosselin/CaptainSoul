# -*- coding: utf-8 -*-

import gtk

from .. import Icons
from ChatView import ChatView


class ChatWindow(gtk.Window):
    _typing = False

    def __init__(self, manager, login, iconify):
        super(ChatWindow, self).__init__()
        self.set_properties(title="CaptainSoul - %s" % login, border_width=2, icon=Icons.shield.get_pixbuf())
        self._manager = manager
        self._login = login
        self._createUi()
        self.connect("delete-event", self.deleteEvent)
        self.connect("delete-event", manager.closeChatWindowEvent, login)
        manager.connect('msg', self.msgEvent)
        manager.connect('is-typing', self.isTypingEvent)
        manager.connect('cancel-typing', self.cancelTypingEvent)
        self.resize(200, 200)
        if iconify:
            self.iconify()
        self.show_all()

    def _createUi(self):
        box = gtk.VBox(False, 0)
        self._text = ChatView()
        box.add(self._text)
        # is typing bar
        self._status = gtk.Statusbar()
        box.pack_start(self._status, False, False, 0)
        # user entry
        view = gtk.TextView()
        view.set_properties(editable=True, cursor_visible=True, wrap_mode=gtk.WRAP_WORD_CHAR)
        self._entry = view.get_buffer()
        view.set_size_request(100, 30)
        view.connect("key-press-event", self.keyPressEvent)
        self._entry.connect("changed", self.keyPressEventEnd)
        box.pack_start(view, False, False, 0)
        self.add(box)

    def deleteEvent(self, widget, reason):
        if self._typing:
            self._typing = False
            self._manager.sendCancelTyping([self._login])

    def keyPressEvent(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == 'Return':
            text = self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True)
            if len(text):
                self._entry.delete(self._entry.get_start_iter(), self._entry.get_end_iter())
                self._text.addMyMsg(text)
                self._manager.sendMsg(text, [self._login])
            return True

    def keyPressEventEnd(self, widget):
        l = len(self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True))
        if not self._typing and l >= 5:
            self._manager.sendStartTyping([self._login])
            self._typing = True
        elif self._typing and l < 5:
            self._manager.sendCancelTyping([self._login])
            self._typing = False

    def addMsg(self, msg):
        self._text.addOtherMsg(msg, self._login)

    def msgEvent(self, widget, info, msg, dests):
        if info.login == self._login:
            self.addMsg(msg)

    def isTypingEvent(self, widget, info):
        if info.login == self._login:
            self._status.push(0, "Is typing...")

    def cancelTypingEvent(self, widget, info):
        if info.login == self._login:
            self._status.remove_all(0)
