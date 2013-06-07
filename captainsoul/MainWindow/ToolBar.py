# -*- coding: utf-8 -*-

import gtk


class ToolBar(gtk.Toolbar):
    def __init__(self, manager):
        super(ToolBar, self).__init__()
        self._manager = manager
        items = []
        # Connection/Deconnection Button
        self._coButton = gtk.ToolButton(gtk.STOCK_CONNECT)
        self._coButton.set_tooltip_text("Connect")
        self._coButtonClicked = self._coButton.connect("clicked", manager.connectEvent)
        items.append(self._coButton)
        # Settings Button
        button = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        button.set_tooltip_text("Settings")
        button.connect("clicked", manager.openSettingsWindowEvent)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Add Contact Button
        button = gtk.ToolButton(gtk.STOCK_ADD)
        button.set_tooltip_text("Add contact")
        button.connect("clicked", manager.openAddContactWindowEvent)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Quit Button
        button = gtk.ToolButton(gtk.STOCK_QUIT)
        button.set_tooltip_text("Quit")
        button.connect("clicked", manager.quitEvent)
        items.append(button)
        # Insert all in the ToolBar
        manager.connect('connecting', self.connectedEvent)
        manager.connect('reconnecting', self.connectedEvent)
        manager.connect('connected', self.connectedEvent)
        manager.connect('disconnected', self.disconnectedEvent)
        for n, item in enumerate(items):
            self.insert(item, n)

    def connectedEvent(self, *args, **kwargs):
        self._coButton.set_stock_id(gtk.STOCK_DISCONNECT)
        self._coButton.set_tooltip_text("Disconnect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._manager.disconnectEvent)

    def disconnectedEvent(self, *args, **kwargs):
        self._coButton.set_stock_id(gtk.STOCK_CONNECT)
        self._coButton.set_tooltip_text("Connect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._manager.connectEvent)
