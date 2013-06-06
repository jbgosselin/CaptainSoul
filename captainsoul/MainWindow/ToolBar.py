# -*- coding: utf-8 -*-

from gi.repository import Gtk


class ToolBar(Gtk.Toolbar):
    def __init__(self, mw):
        super(ToolBar, self).__init__()
        self._mw = mw
        items = []
        # Connection/Deconnection Button
        self._coButton = Gtk.ToolButton(Gtk.STOCK_CONNECT, tooltip_text="Connect")
        self._coButtonClicked = self._coButton.connect("clicked", self._mw.connectEvent)
        items.append(self._coButton)
        # Settings Button
        button = Gtk.ToolButton(Gtk.STOCK_PREFERENCES, tooltip_text="Settings")
        button.connect("clicked", self._mw.settingsEvent)
        items.append(button)
        # Separator
        items.append(Gtk.SeparatorToolItem())
        # Add Contact Button
        button = Gtk.ToolButton(Gtk.STOCK_ADD, tooltip_text="Add contact")
        button.connect("clicked", self._mw.addContactWindowEvent)
        items.append(button)
        # Separator
        items.append(Gtk.SeparatorToolItem())
        # Quit Button
        button = Gtk.ToolButton(Gtk.STOCK_QUIT, tooltip_text="Quit")
        button.connect("clicked", self._mw.quitEvent)
        items.append(button)
        # Insert all in the ToolBar
        for n, item in enumerate(items):
            self.insert(item, n)

    def connectEvent(self):
        self._coButton.set_stock_id(Gtk.STOCK_DISCONNECT)
        self._coButton.set_tooltip_text("Disconnect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._mw.disconnectEvent)

    def disconnectEvent(self):
        self._coButton.set_stock_id(Gtk.STOCK_CONNECT)
        self._coButton.set_tooltip_text("Connect")
        self._coButton.disconnect(self._coButtonClicked)
        self._coButtonClicked = self._coButton.connect("clicked", self._mw.connectEvent)
