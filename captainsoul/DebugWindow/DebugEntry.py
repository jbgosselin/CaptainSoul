# -*- coding: utf-8 -*-

import gtk


class DebugEntry(gtk.Entry):
    def __init__(self, manager):
        super(DebugEntry, self).__init__()
        self.connect('activate', self.activateEvent, manager)

    def activateEvent(self, widget, manager):
        line = widget.get_text()
        if line:
            widget.set_text('')
            manager.sendRaw(line)
