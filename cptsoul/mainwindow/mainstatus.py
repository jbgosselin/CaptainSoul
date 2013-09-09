# -*- coding: utf-8 -*-

import gtk

from cptsoul.common import CptCommon


class MainStatus(gtk.Statusbar, CptCommon):
    def __init__(self):
        super(MainStatus, self).__init__()
        self.push(0, 'Welcome')
        self.manager.connect('logged', self.loggedEvent)
        self.manager.connect('reconnecting', self.reconnectingEvent)
        self.manager.connect('disconnected', self.disconnectedEvent)
        self.manager.connect('connecting', self.connectingEvent)

    def connectingEvent(self, widget):
        self.push(0, "Connecting...")

    def loggedEvent(self, widget):
        self.push(0, "Connected")

    def reconnectingEvent(self, widget):
        self.push(0, "Reconnecting...")

    def disconnectedEvent(self, widget):
        self.push(0, "Disconnected")
