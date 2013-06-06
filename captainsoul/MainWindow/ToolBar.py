# -*- coding: utf-8 -*-

from gi.repository import Gtk


class ToolBar(Gtk.Toolbar):
    def __init__(self, manager):
        super(ToolBar, self).__init__()
        self._manager = manager
        items = []
        # Connection/Deconnection Button
        self._coButton = Gtk.ToolButton(stock_id=Gtk.STOCK_CONNECT, tooltip_text="Connect")
        self._coButtonClicked = self._coButton.connect("clicked", manager.connectEvent)
        items.append(self._coButton)
        # Settings Button
        button = Gtk.ToolButton(stock_id=Gtk.STOCK_PREFERENCES, tooltip_text="Settings")
        button.connect("clicked", manager.openSettingsWindowEvent)
        items.append(button)
        # Separator
        items.append(Gtk.SeparatorToolItem())
        # Add Contact Button
        button = Gtk.ToolButton(stock_id=Gtk.STOCK_ADD, tooltip_text="Add contact")
        button.connect("clicked", manager.openAddContactWindowEvent)
        items.append(button)
        # Separator
        items.append(Gtk.SeparatorToolItem())
        # Quit Button
        button = Gtk.ToolButton(stock_id=Gtk.STOCK_QUIT, tooltip_text="Quit")
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
        self._coButton.set_stock_id(Gtk.STOCK_DISCONNECT)
        self._coButton.set_tooltip_text("Disconnect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._manager.disconnectEvent)

    def disconnectedEvent(self, *args, **kwargs):
        self._coButton.set_stock_id(Gtk.STOCK_CONNECT)
        self._coButton.set_tooltip_text("Connect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._manager.connectEvent)
