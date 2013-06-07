# -*- coding: utf-8 -*-

import gtk

import Icons


class AddContactWindow(gtk.Dialog):
    def __init__(self):
        super(AddContactWindow, self).__init__(title="CaptainSoul - Add contact")
        self.set_properties(border_width=2, icon=Icons.shield.get_pixbuf())
        self._createUi()
        self.show_all()

    def activateEvent(self, *args, **kwargs):
        self.response(gtk.RESPONSE_OK)

    def getLogin(self):
        return self._entry.get_text().strip()

    def _createUi(self):
        self._entry = gtk.Entry()
        self._entry.connect("activate", self.activateEvent)
        self.vbox.pack_start(self._entry, True, True, 0)
        self.add_button("Ok", gtk.RESPONSE_OK)
        self.add_button("Cancel", gtk.RESPONSE_CANCEL)
