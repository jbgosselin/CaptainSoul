# -*- coding: utf-8 -*-

from gi.repository import Gtk, Pango


class ChatView(Gtk.ScrolledWindow):
    def __init__(self):
        super(ChatView, self).__init__(border_width=0)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self._box = Gtk.VBox(False, 0)
        self.add(self._box)
        self.show_all()

    def addMsg(self, msg, xalign):
        label = Gtk.Label(label=msg, wrap=True, wrap_mode=Pango.WrapMode.WORD_CHAR, selectable=True, justify=Gtk.Justification.LEFT, yalign=0, xalign=xalign)
        self._box.pack_start(label, False, False, 0)
        label.show()

    def addOtherMsg(self, msg, login):
        self.addMsg(msg, 0)

    def addMyMsg(self, msg):
        self.addMsg(msg, 1)
