# -*- coding: utf-8 -*-

import gtk


class DebugView(gtk.ScrolledWindow):
    def __init__(self, manager):
        super(DebugView, self).__init__()
        self.set_properties(
            border_width=0,
            shadow_type=gtk.SHADOW_ETCHED_IN,
            hscrollbar_policy=gtk.POLICY_AUTOMATIC,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC
        )
        self._createUi()
        manager.connect('send-raw', self.sendRawEvent)
        manager.connect('get-raw', self.getRawEvent)
        self._buffer.connect('changed', self.bufferChangedEvent)

    def _createUi(self):
        textview = gtk.TextView()
        textview.set_properties(
            cursor_visible=False,
            editable=False,
            wrap_mode=gtk.WRAP_WORD_CHAR
        )
        self._buffer = textview.get_buffer()
        self.add(textview)

    def printLine(self, line):
        self._buffer.insert(self._buffer.get_end_iter(), "%s\n" % line)

    def getRawEvent(self, widget, line):
        self.printLine(">> %s" % line)

    def sendRawEvent(self, widget, line):
        self.printLine('<< %s' % line)

    def bufferChangedEvent(self, widget):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper())
