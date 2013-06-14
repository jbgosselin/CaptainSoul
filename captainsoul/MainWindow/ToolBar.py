# -*- coding: utf-8 -*-

import gtk


class ToolBar(gtk.Toolbar):
    def __init__(self, manager):
        super(ToolBar, self).__init__()
        items = []
        # Connection/Deconnection Button
        coButton = gtk.ToolButton(gtk.STOCK_CONNECT)
        coButton.set_properties(
            tooltip_text="Connect",
            label="Connect"
        )
        self._coButtonClicked = coButton.connect("clicked", manager.connectEvent)
        items.append(coButton)
        # Settings Button
        button = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        button.set_properties(
            tooltip_text="Settings",
            label="Settings"
        )
        button.connect("clicked", manager.openSettingsWindowEvent)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Add Contact Button
        button = gtk.ToolButton(gtk.STOCK_ADD)
        button.set_properties(
            tooltip_text="Add contact",
            label="Add contact"
        )
        button.connect("clicked", manager.openAddContactWindowEvent)
        items.append(button)
        # Open download manager
        button = gtk.ToolButton(gtk.STOCK_SAVE)
        button.set_properties(
            tooltip_text="Downloads",
            label="Downloads"
        )
        button.connect("clicked", self.openDownloadEvent, manager)
        items.append(button)
        # Separator
        items.append(gtk.SeparatorToolItem())
        # Quit Button
        button = gtk.ToolButton(gtk.STOCK_QUIT)
        button.set_properties(
            tooltip_text="Quit",
            label="Quit"
        )
        button.connect("clicked", manager.quitEvent)
        items.append(button)
        # Insert all in the ToolBar
        manager.connect('connecting', self.connectedEvent, coButton, manager)
        manager.connect('reconnecting', self.connectedEvent, coButton, manager)
        manager.connect('connected', self.connectedEvent, coButton, manager)
        manager.connect('disconnected', self.disconnectedEvent, coButton, manager)
        for n, item in enumerate(items):
            self.insert(item, n)

    def connectedEvent(self, widget, button, manager):
        button.set_stock_id(gtk.STOCK_DISCONNECT)
        button.set_properties(
            tooltip_text="Disconnect",
            label="Disconnect"
        )
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect("clicked", manager.disconnectEvent)

    def disconnectedEvent(self, widget, button, manager):
        button.set_stock_id(gtk.STOCK_CONNECT)
        button.set_properties(
            tooltip_text="Connect",
            label="Connect"
        )
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect("clicked", manager.connectEvent)

    def openDownloadEvent(self, widget, manager):
        manager._downloadManager.show_all()
        manager._downloadManager.present()
