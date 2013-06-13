# -*- coding: utf-8 -*-

import re
import webbrowser

import gtk
import pango


class ChatView(gtk.ScrolledWindow):
    http_regex = re.compile(r"https?://[\w\-\.~\:/\?#\[\]@!$&'\(\)\*\+,;=%]+")

    def __init__(self, manager, login, msg=None):
        super(ChatView, self).__init__()
        self.set_properties(
            border_width=0,
            shadow_type=gtk.SHADOW_ETCHED_IN,
            hscrollbar_policy=gtk.POLICY_AUTOMATIC,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC
        )
        self._createUi()
        self.connect('destroy', self.destroyEvent, manager)
        self._connections = [
            manager.connect('msg', self.msgEvent, login),
            manager.connect('send-msg', self.sendMsgEvent, login)
        ]
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
        textview.connect('event-after', self.eventAfterEvent)
        self._buffer = textview.get_buffer()
        self.add(textview)

    def eventAfterEvent(self, widget, event):
        if event.type != gtk.gdk.BUTTON_RELEASE or event.button != 1:
            return False
        try:
            start, end = self._buffer.get_selection_bounds()
        except ValueError:
            pass
        else:
            if start.get_offset() != end.get_offset():
                return False
        x, y = widget.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET, int(event.x), int(event.y))
        it = widget.get_iter_at_location(x, y)
        tags = it.get_tags()
        for tag in tags:
            link = tag.get_data("link")
            if link:
                webbrowser.open_new_tab(link)

    def insertLink(self, link):
        tag = self._buffer.create_tag(None, foreground="blue", underline=pango.UNDERLINE_SINGLE)
        tag.set_data("link", link)
        self._buffer.insert_with_tags(self._buffer.get_end_iter(), link, tag)

    def insertText(self, text):
        self._buffer.insert_with_tags(self._buffer.get_end_iter(), text)

    def printMsg(self, login, msg):
        self.insertText("[%s] : " % login)
        f = self.http_regex.search(msg)
        while f:
            start, end = f.start(), f.end()
            if start > 0:
                self.insertText(msg[:start])
                self.insertLink(msg[start:end])
            else:
                self.insertLink(msg[:end])
            msg = msg[end:]
            f = self.http_regex.search(msg)
        self.insertText('%s\n' % msg)

    def msgEvent(self, widget, info, msg, dests, login):
        if login == info.login:
            self.printMsg(login, msg)

    def sendMsgEvent(self, widget, msg, dests, login):
        if login in dests:
            self.printMsg('Me', msg)

    def bufferChangedEvent(self, widget):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper())

    def destroyEvent(self, widget, manager):
        for co in self._connections:
            manager.disconnect(co)
