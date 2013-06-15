# -*- coding: utf-8 -*-

import gtk

from DebugView import DebugView
from DebugEntry import DebugEntry


class DebugWindow(gtk.Window):
    def __init__(self, manager):
        super(DebugWindow, self).__init__()
        self.set_properties(
            title="CaptainSoul - Debug"
        )
        self._createUi(manager)
        self.show_all()

    def _createUi(self, manager):
        box = gtk.VBox(False, 0)
        self.add(box)
        # chatview
        box.add(DebugView(manager))
        # user entry
        entry = DebugEntry(manager)
        box.pack_start(entry, False, False, 0)
