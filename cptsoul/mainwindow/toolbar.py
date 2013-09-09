# -*- coding: utf-8 -*-

import gtk

from cptsoul.common import CptCommon


class ToolBar(gtk.Toolbar, CptCommon):
    def __init__(self):
        super(ToolBar, self).__init__()
        items = []
        # Connection/Deconnection Button
        coButton = gtk.ToolButton(gtk.STOCK_CONNECT)
        coButton.set_properties(
            tooltip_text="Connect",
            label="Connect"
        )
        self._coButtonClicked = coButton.connect("clicked", self.manager.connectEvent)
        items.append(coButton)
        # Settings Button
        button = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        button.set_properties(
            tooltip_text="Settings",
            label="Settings"
        )
        button.connect("clicked", self.manager.openSettingsWindowEvent)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Add Contact Button
        button = gtk.ToolButton(gtk.STOCK_ADD)
        button.set_properties(
            tooltip_text="Add contact",
            label="Add contact"
        )
        button.connect("clicked", self.manager.openAddContactWindowEvent)
        items.append(button)
        # Open download manager
        button = gtk.ToolButton(gtk.STOCK_SAVE)
        button.set_properties(
            tooltip_text="Downloads",
            label="Downloads"
        )
        button.connect("clicked", self.openDownloadEvent)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Quit Button
        button = gtk.ToolButton(gtk.STOCK_QUIT)
        button.set_properties(
            tooltip_text="Quit",
            label="Quit"
        )
        button.connect("clicked", self.manager.quitEvent)
        items.append(button)
        # Insert all in the ToolBar
        self.manager.connect('connecting', self.connectedEvent, coButton)
        self.manager.connect('reconnecting', self.connectedEvent, coButton)
        self.manager.connect('connected', self.connectedEvent, coButton)
        self.manager.connect('disconnected', self.disconnectedEvent, coButton)
        for n, item in enumerate(items):
            self.insert(item, n)

    def connectedEvent(self, widget, button):
        button.set_stock_id(gtk.STOCK_DISCONNECT)
        button.set_properties(
            tooltip_text="Disconnect",
            label="Disconnect"
        )
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect("clicked", self.manager.disconnectEvent)

    def disconnectedEvent(self, widget, button):
        button.set_stock_id(gtk.STOCK_CONNECT)
        button.set_properties(
            tooltip_text="Connect",
            label="Connect"
        )
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect("clicked", self.manager.connectEvent)

    def openDownloadEvent(self, widget):
        self.downloadManager.show_all()
        self.downloadManager.present()
