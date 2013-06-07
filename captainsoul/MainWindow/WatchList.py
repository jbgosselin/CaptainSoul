# -*- coding: utf-8 -*-

import gtk

from ..Config import Config
from .. import Icons


class Buddy(object):
    def __init__(self, no, login, state, ip, location):
        self._no, self._login, self._state, self._ip, self._location = int(no), login, state, ip, location

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
    def __init__(self):
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


class WatchList(gtk.TreeView):
    _loginColumn = 1

    def __init__(self, manager):
        self._listStore = gtk.ListStore(gtk.gdk.Pixbuf, str, gtk.gdk.Pixbuf, str)
        super(WatchList, self).__init__(model=self._listStore)
        self._manager, self._list = manager, LoginList()
        self._listStore.set_sort_column_id(self._loginColumn, gtk.SORT_ASCENDING)
        columns = [
            gtk.TreeViewColumn("State", gtk.CellRendererPixbuf(), pixbuf=0),
            gtk.TreeViewColumn("Login", gtk.CellRendererText(), text=self._loginColumn),
            gtk.TreeViewColumn("At school", gtk.CellRendererPixbuf(), pixbuf=2),
            gtk.TreeViewColumn("", gtk.CellRendererText(), text=3)
        ]
        for column in columns:
            self.append_column(column)
        self.connect("row-activated", self.rowActivated)
        self.connect("button-press-event", self.buttonPressEvent)
        manager.connect('state', self.stateEvent)
        manager.connect('contact-added', self.contactAddedEvent)
        manager.connect('contact-deleted', self.contactDeletedEvent)
        manager.connect('who', self.whoEvent)
        manager.connect('logout', self.logoutEvent)
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

    def stateEvent(self, widget, info, state):
        self._list.changeState(info, state)
        self.refreshStore()

    def contactAddedEvent(self, widget, login):
        self._list.clean()
        self.refreshStore()

    def contactDeletedEvent(self, widget, login):
        self._list.clean()
        self.refreshStore()

    def rowActivated(self, tv, path, column):
        self._manager.doOpenChat(self._listStore.get_value(self._listStore.get_iter(path), self._loginColumn))

    def buttonPressEvent(self, wid, event):
        # 3 is right click
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            path = self.get_path_at_pos(int(event.x), int(event.y))
            if path is not None:
                login = self._listStore.get_value(self._listStore.get_iter(path[0]), self._loginColumn)
                self._menu = gtk.Menu()
                item = gtk.ImageMenuItem()
                item.set_label(gtk.STOCK_DELETE)
                item.set_use_stock(True)
                item.connect("activate", self.deleteContactEvent, login)
                item.show()
                self._menu.append(item)
                self._menu.popup(None, None, None, event.button, event.time)

    def deleteContactEvent(self, widget, login):
        self._manager.doDeleteContact(login)

    def whoEvent(self, widget, results):
        self._list.processWho(results)
        self.refreshStore()

    def logoutEvent(self, widget, info):
        self._list.logout(info)
        self.refreshStore()
