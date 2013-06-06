# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk

from ..Config import Config
from .. import Icons


class Buddy(object):
    def __init__(self, no, login, state, ip, location):
        self._no = int(no)
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

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<Buddy %d %s %s %s "%s">' % (self.no, self.login, self.state, self.ip, self.location)


class LoginList(object):
    _list = {}

    def clean(self):
        self._list = {no: buddy for no, buddy in self._list.iteritems() if buddy.login in Config['watchlist']}

    def processWho(self, results):
        for r in results:
            if r.login in Config['watchlist']:
                self._list[r.no] = Buddy(r.no, r.login, r.state, r.ip, r.location)

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
        if info.login in Config['watchlist']:
            if info.no in self._list:
                self._list[info.no].state = state
            else:
                self._list[info.no] = Buddy(info.no, info.login, state, info.ip, info.location)

    def logout(self, info):
        if info.no in self._list:
            del self._list[info.no]


class WatchList(Gtk.TreeView):
    _list = LoginList()
    _loginColumn = 1

    def __init__(self, mw):
        self._listStore = Gtk.ListStore(GdkPixbuf.Pixbuf, str, GdkPixbuf.Pixbuf, str)
        super(WatchList, self).__init__(model=self._listStore)
        self._manager = mw._manager
        self._mw = mw
        self._listStore.set_sort_column_id(self._loginColumn, Gtk.SortType.ASCENDING)
        columns = [
            Gtk.TreeViewColumn("State", Gtk.CellRendererPixbuf(), pixbuf=0),
            Gtk.TreeViewColumn("Login", Gtk.CellRendererText(), text=self._loginColumn),
            Gtk.TreeViewColumn("At school", Gtk.CellRendererPixbuf(), pixbuf=2),
            Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=3)
        ]
        for column in columns:
            self.append_column(column)
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
            self._listStore.append([
                pix,
                login,
                Icons.epitech.get_pixbuf() if atSchool else Icons.void.get_pixbuf(),
                "",
            ])

    def setState(self, info, state):
        self._list.changeState(info, state)
        self.refreshStore()

    def addContact(self, login):
        Config['watchlist'].add(login)
        self._list.clean()
        self.refreshStore()
        self._mw.sendWatch()

    def deleteContactEvent(self, widget, login):
        Config['watchlist'].remove(login)
        self._list.clean()
        self.refreshStore()
        self._mw.sendWatch(False)

    def rowActivated(self, tv, path, column):
        self._manager.openWindow(self._listStore.get_value(self._listStore.get_iter(path), self._loginColumn))

    def buttonPressEvent(self, wid, event):
        # 3 is right click
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            path = self.get_path_at_pos(event.x, event.y)
            if path is not None:
                login = self._listStore.get_value(self._listStore.get_iter(path[0]), self._loginColumn)
                self._menu = Gtk.Menu()
                item = Gtk.ImageMenuItem(label=Gtk.STOCK_DELETE)
                item.set_use_stock(True)
                item.connect("activate", self.deleteContactEvent, login)
                item.show()
                self._menu.append(item)
                self._menu.popup(None, None, None, None, event.button, event.time)

    def processWho(self, results):
        self._list.processWho(results)
        self.refreshStore()

    def logoutHook(self, info):
        self._list.logout(info)
        self.refreshStore()
