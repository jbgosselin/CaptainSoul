# -*- coding: utf-8 -*-

from gi.repository import Gtk, Pango, Gdk

import Icons


class ChatWindow(Gtk.Window):
    _typing = False

    def __init__(self, manager, mw, login, iconify):
        super(ChatWindow, self).__init__(title="CaptainSoul - %s" % login, border_width=2, icon=Icons.shield.get_pixbuf())
        self._login = login
        self._mw = mw
        self._createUi()
        self._text.create_tag("bold", weight=Pango.Weight.BOLD)
        self.connect("delete-event", self.deleteEvent)
        self.connect("delete-event", manager.closeWindow, login)
        self.resize(200, 200)
        if iconify:
            self.iconify()
        self.show_all()

    def _createUi(self):
        box = Gtk.VBox(False, 0)
        scroll = Gtk.ScrolledWindow(Gtk.Adjustment(200, 200, 200))
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(200, 200)
        view = Gtk.TextView(editable=False, cursor_visible=False, wrap_mode=Gtk.WrapMode.WORD)
        self._text = view.get_buffer()
        scroll.add_with_viewport(view)
        box.pack_start(scroll, True, True, 0)
        view = Gtk.TextView(editable=True, cursor_visible=True, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        self._entry = view.get_buffer()
        view.set_size_request(100, 30)
        view.connect("key-press-event", self.keyPressEvent)
        self._entry.connect("changed", self.keyPressEventEnd)
        box.pack_start(view, False, False, 10)
        self._status = Gtk.Statusbar()
        box.pack_start(self._status, False, False, 0)
        self.add(box)

    def deleteEvent(self, widget, reason):
        if self._typing:
            self._mw.sendCancelTyping([self._login])
            self._typing = False

    def keyPressEvent(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            text = self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True)
            if len(text):
                self._entry.delete(self._entry.get_start_iter(), self._entry.get_end_iter())
                self._mw.sendMsg(text, [self._login])
                self._printOn("Me", text)
            return True

    def keyPressEventEnd(self, widget):
        l = len(self._entry.get_text(self._entry.get_start_iter(), self._entry.get_end_iter(), True))
        if not self._typing and l >= 5:
            self._mw.sendStartTyping([self._login])
            self._typing = True
        elif self._typing and l < 5:
            self._mw.sendCancelTyping([self._login])
            self._typing = False

    def _printOn(self, name, msg):
        self._text.insert_with_tags_by_name(self._text.get_end_iter(), "%s: " % name, "bold")
        self._text.insert(self._text.get_end_iter(), "%s\n" % msg)

    def addMsg(self, msg):
        self._printOn(self._login, msg)

    def changeState(self, state):
        pass

    def startTyping(self):
        self._status.push(0, "Is typing...")

    def cancelTyping(self):
        self._status.remove_all(0)
