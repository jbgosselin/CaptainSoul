# -*- coding: utf-8 -*-

from gi.repository import Gtk

from Config import Config
import Icons


class SettingsWindow(Gtk.Dialog):
    def __init__(self):
        super(SettingsWindow, self).__init__(title="CaptainSoul - Settings", border_width=2, icon=Icons.shield.get_pixbuf())
        self._createUi()
        self.show_all()
        if self.run() == Gtk.ResponseType.APPLY:
            Config.login = self._loginEntry.get_text()
            Config.password = self._passwordEntry.get_text()
            Config.location = self._locationEntry.get_text()
            Config.autoConnect = self._autoButton.get_active()

    def _createUi(self):
        table = Gtk.Table(4, 3, True)
        table.attach(Gtk.Label("Login:"), 0, 1, 0, 1)
        self._loginEntry = Gtk.Entry(text=Config.login)
        table.attach(self._loginEntry, 1, 3, 0, 1)
        table.attach(Gtk.Label("Password:"), 0, 1, 1, 2)
        self._passwordEntry = Gtk.Entry(text=Config.password, visibility=False)
        table.attach(self._passwordEntry, 1, 3, 1, 2)
        table.attach(Gtk.Label("Location:"), 0, 1, 2, 3)
        self._locationEntry = Gtk.Entry(text=Config.location)
        table.attach(self._locationEntry, 1, 3, 2, 3)
        table.attach(Gtk.Label("Auto-connect:"), 0, 2, 3, 4)
        self._autoButton = Gtk.CheckButton(active=Config.autoConnect)
        table.attach(self._autoButton, 2, 3, 3, 4)
        self.vbox.pack_start(table, True, True, 0)
        self.add_button("Apply", Gtk.ResponseType.APPLY)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
