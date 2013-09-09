# -*- coding: utf-8 -*-

import gtk

from cptsoul.common import CptCommon


class DebugEntry(gtk.Entry, CptCommon):
    def __init__(self):
        super(DebugEntry, self).__init__()
        self.connect('activate', self.activateEvent)

    def activateEvent(self, widget):
        line = widget.get_text()
        if line:
            widget.set_text('')
            self.manager.sendRaw(line)
