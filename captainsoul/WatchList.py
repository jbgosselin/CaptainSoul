# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf

from Config import Config
import Icons


class WatchList(Gtk.TreeView):
    _list = {}

    def __init__(self, mw):
        self._listStore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        super(WatchList, self).__init__(model=self._listStore)
        self.set_headers_visible(False)
        self._manager = mw._manager
        self._listStore.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self.append_column(Gtk.TreeViewColumn("State", Gtk.CellRendererPixbuf(), pixbuf=0))
        self.append_column(Gtk.TreeViewColumn("Login", Gtk.CellRendererText(), text=1))
        self.connect("row-activated", self.rowActivated)
        self.updateWatchlist()
        self.refreshStore()

    def refreshStore(self):
        self._listStore.clear()
        for contact, state in self._list.iteritems():
            if state == 'actif':
                pix = Icons.green.get_pixbuf()
            elif state in ('away', 'lock'):
                pix = Icons.red.get_pixbuf()
            else:
                pix = Icons.void.get_pixbuf()
            self._listStore.append([pix, contact])

    def setState(self, login, state):
        if login in self._list:
            self._list[login] = state
            self.refreshStore()

    def updateWatchlist(self):
        self._list = {contact: self._list.get(contact, 'logout') for contact in Config['watchlist']}
        self.refreshStore()

    def addContact(self, login):
        Config['watchlist'].add(login)
        self.updateWatchlist()

    def rowActivated(self, tv, path, column):
        self._manager.openWindow(self._listStore.get_value(self._listStore.get_iter(path), 1))
