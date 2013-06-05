# -*- coding: utf-8 -*-

from gi.repository import Gtk

import Icons


class AddContactWindow(Gtk.Dialog):
    def __init__(self, mw):
        super(AddContactWindow, self).__init__(title="CaptainSoul - Add contact", border_width=2, icon=Icons.shield.get_pixbuf())
        self._createUi()
        self.show_all()
        if self.run() == Gtk.ResponseType.OK:
            login = self._entry.get_text().strip()
            if login:
                mw._watchlist.addContact(login)

    def activateEvent(self, *args, **kwargs):
        self.response(Gtk.ResponseType.OK)

    def _createUi(self):
        self._entry = Gtk.Entry()
        self._entry.connect("activate", self.activateEvent)
        self.vbox.pack_start(self._entry, True, True, 0)
        self.add_button("Ok", Gtk.ResponseType.OK)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
