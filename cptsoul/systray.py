# -*- coding: utf-8 -*-

import gtk

from cptsoul import icons
from cptsoul.common import CptCommon
from cptsoul.notify import Notifier


class Systray(gtk.StatusIcon, CptCommon):
    def __init__(self):
        super(Systray, self).__init__()
        self._reconnecting = False
        self._notifier = Notifier()
        self.set_from_pixbuf(icons.shield)
        self.set_properties(
            tooltip_text="CaptainSoul",
            visible=True
        )
        self.connect("activate", self.mainWindow.showHideEvent)
        self.manager.connect('msg', self.msgEvent)
        self.manager.connect('logged', self.loggedEvent)
        self.manager.connect('reconnecting', self.reconnectingEvent)

    def msgEvent(self, widget, info, msg, dests):
        self._notifier.notify("CaptainSoul - New message from %s" % info.login, msg, 'dialog-information')

    def loggedEvent(self, widget):
        self._reconnecting = False
        self._notifier.notify('CaptainSoul', 'Connected', 'dialog-ok')

    def reconnectingEvent(self, widget):
        if not self._reconnecting:
            self._notifier.notify('CaptainSoul', 'Connection lost, reconnecting', 'dialog-warning')
            self._reconnecting = True
