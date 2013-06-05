# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk

from Config import Config
import Icons


class Buddy(object):
    def __init__(self, no, login, state, ip, location):
        self._no = no
        self._login = login
        self._state = state
        self._ip = ip
        self._location = location

    @property
    def no(self):
        return self._no

    @property
    def login(self):
        return self._login

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def ip(self):
        return self._ip

    @property
    def location(self):
        return self._location

    def atSchool(self):
        return self._ip.startswith('10.')


class LoginList(object):
    _list = {}

    def clean(self):
        self._list = {no: buddy for no, buddy in self._list.iteritems() if buddy.login in Config['watchlist']}

    def processWho(self, results):
        self._list = {r.no: Buddy(r.no, r.login, r.state, r.ip, r.location) for r in results if r.login in Config['watchlist']}

    def formatWatchList(self):
        return [(self.getState(login), login, self.atSchool(login)) for login in Config['watchlist']]

    def getFromLogin(self, login):
        return [buddy for buddy in self._list.itervalues() if buddy.login == login]

    def getState(self, login):
        state = 'logout'
        for buddy in self.getFromLogin(login):
            if state == 'logout' and buddy.state in ('away', 'lock', 'actif') or state in ('away', 'lock') and buddy.state == 'actif':
                state = buddy.state
        return state

    def atSchool(self, login):
        return any([buddy.atSchool() for buddy in self.getFromLogin(login)])

    def changeState(self, info, state):
        if info.no in self._list:
            self._list[info.no].state = state

    def logout(self, info):
        if info.no in self._list:
            del self._list[info.no]


class WatchList(Gtk.TreeView):
    _list = LoginList()

    def __init__(self, mw):
        self._listStore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        super(WatchList, self).__init__(model=self._listStore)
        self.set_headers_visible(False)
        self._manager = mw._manager
        self._mw = mw
        self._listStore.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        self.append_column(Gtk.TreeViewColumn("State", Gtk.CellRendererPixbuf(), pixbuf=0))
        self.append_column(Gtk.TreeViewColumn("Login", Gtk.CellRendererText(), text=1))
        self.connect("row-activated", self.rowActivated)
        self.connect("button-press-event", self.buttonPressEvent)
        self.refreshStore()

    def refreshStore(self):
        self._listStore.clear()
        for state, login, atSchool in self._list.formatWatchList():
            if state == 'actif':
                pix = Icons.green.get_pixbuf()
            elif state in ('away', 'lock'):
                pix = Icons.red.get_pixbuf()
            else:
                pix = Icons.void.get_pixbuf()
            self._listStore.append([pix, login])

    def setState(self, info, state):
        self._list.changeState(info, state)
        self.refreshStore()

    def addContact(self, login):
        Config['watchlist'].add(login)
        self._list.clean()
        self.refreshStore()

    def deleteContactEvent(self, widget, login):
        Config['watchlist'].remove(login)
        self.clean()
        self.refreshStore()
        self._mw.sendWatch()

    def rowActivated(self, tv, path, column):
        self._manager.openWindow(self._listStore.get_value(self._listStore.get_iter(path), 1))

    def buttonPressEvent(self, wid, event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == Gdk.BUTTON_SECONDARY:
            path = self.get_path_at_pos(event.x, event.y)
            if path is not None:
                login = self._listStore.get_value(self._listStore.get_iter(path[0]), 1)
                self._menu = Gtk.Menu()
                item = Gtk.ImageMenuItem(label=Gtk.STOCK_DELETE, use_stock=True)
                item.connect("activate", self.deleteContactEvent, login)
                item.show()
                self._menu.append(item)
                self._menu.popup(None, None, None, None, event.button, event.time)

    def processWho(self, results):
        self._list.processWho(results)
        self.refreshStore()
