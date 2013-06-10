# -*- coding: utf-8 -*-

import gtk


class ChatView(gtk.ScrolledWindow):
    def __init__(self, manager, login, msg=None):
        super(ChatView, self).__init__()
        self.set_properties(
            border_width=0,
            shadow_type=gtk.SHADOW_ETCHED_IN,
            hscrollbar_policy=gtk.POLICY_AUTOMATIC,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC
        )
        self._createUi()
        manager.connect('msg', self.msgEvent, login)
        manager.connect('send-msg', self.sendMsgEvent, login)
        self._buffer.connect('changed', self.bufferChangedEvent)
        if msg is not None:
            self.printMsg(login, msg)

    def _createUi(self):
        textview = gtk.TextView()
        textview.set_properties(
            cursor_visible=False,
            editable=False,
            wrap_mode=gtk.WRAP_WORD_CHAR
        )
        self._buffer = textview.get_buffer()
        self.add(textview)

    def printMsg(self, login, msg):
        self._buffer.insert(self._buffer.get_end_iter(), "[%s] : %s\n" % (login, msg))

    def msgEvent(self, widget, info, msg, dests, login):
        if login == info.login:
            self.printMsg(login, msg)

    def sendMsgEvent(self, widget, msg, dests, login):
        if login in dests:
            self.printMsg('Me', msg)

    def bufferChangedEvent(self, widget):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper())
