# -*- coding: utf-8 -*-

import gtk


class ChatEntry(gtk.TextView):
    def __init__(self, manager, login):
        super(ChatEntry, self).__init__()
        self.set_properties(
            editable=True,
            cursor_visible=True,
            wrap_mode=gtk.WRAP_WORD_CHAR,
            width_request=100,
            height_request=40
        )
        self._typing = False
        self.connect("key-press-event", self.keyPressEvent, manager, login)
        self.get_buffer().connect("changed", self.keyPressEventEnd, manager, login)

    def deleteEvent(self, widget, reason, manager, login):
        if self._typing:
            self._typing = False
            manager.sendCancelTyping([login])

    def keyPressEvent(self, widget, event, manager, login):
        if gtk.gdk.keyval_name(event.keyval) in ('Return', 'KP_Enter'):
            buff = self.get_buffer()
            text = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)
            if len(text):
                buff.delete(buff.get_start_iter(), buff.get_end_iter())
                manager.sendMsg(text, [login])
            return True

    def keyPressEventEnd(self, widget, manager, login):
        buff = self.get_buffer()
        l = len(buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True))
        if not self._typing and l >= 5:
            manager.sendStartTyping([login])
            self._typing = True
        elif self._typing and l < 5:
            manager.sendCancelTyping([login])
            self._typing = False
