# -*- coding: utf-8 -*-

import gtk

from DebugView import DebugView
from DebugEntry import DebugEntry


class DebugWindow(gtk.Window):
    def __init__(self):
        super(DebugWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul - Debug"
        )
        self._createUi()
        self.show_all()

    def _createUi(self):
        box = gtk.VBox(False, 0)
        self.add(box)
        # chatview
        box.add(DebugView())
        # user entry
        entry = DebugEntry()
        box.pack_start(entry, False, False, 0)
