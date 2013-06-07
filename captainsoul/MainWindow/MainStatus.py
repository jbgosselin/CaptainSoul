# -*- coding: utf-8 -*-

import gtk


class MainStatus(gtk.Statusbar):
    def __init__(self, manager):
        super(MainStatus, self).__init__()
        self.push(0, 'Welcome')
        manager.connect('logged', self.loggedEvent)
        manager.connect('reconnecting', self.reconnectingEvent)
        manager.connect('disconnected', self.disconnectedEvent)
        manager.connect('connecting', self.connectingEvent)

    def connectingEvent(self, widget):
        self.push(0, "Connecting...")

    def loggedEvent(self, widget):
        self.push(0, "Connected")

    def reconnectingEvent(self, widget):
        self.push(0, "Reconnecting...")

    def disconnectedEvent(self, widget):
        self.push(0, "Disconnected")
