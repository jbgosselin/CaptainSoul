# -*- coding: utf-8 -*-

import gtk
import pango


class ChatView(gtk.ScrolledWindow):
    def __init__(self):
        super(ChatView, self).__init__()
        self.set_border_width(0)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self._box = gtk.VBox(False, 0)
        self.add_with_viewport(self._box)
        self.show_all()

    def addMsg(self, msg, xalign):
        label = gtk.Label(msg)
        label.set_properties(wrap=True, wrap_mode=pango.WRAP_WORD_CHAR, selectable=True, justify=gtk.JUSTIFY_LEFT, yalign=0, xalign=xalign)
        self._box.pack_start(label, False, False, 0)
        label.show()

    def addOtherMsg(self, msg, login):
        self.addMsg(msg, 0)

    def addMyMsg(self, msg):
        self.addMsg(msg, 1)
