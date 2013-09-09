# -*- coding: utf-8 -*-

import gtk

from cptsoul import icons
from cptsoul.common import CptCommon
from cptsoul.mainwindow.loginlist import LoginList


class WatchList(gtk.TreeView, CptCommon):
    _loginColumn = 1
    pixs = {
        'actif': icons.green,
        'away': icons.orange,
        'lock': icons.red
    }

    def __init__(self):
        super(WatchList, self).__init__(model=gtk.ListStore(gtk.gdk.Pixbuf, str, gtk.gdk.Pixbuf, str))
        self._list = LoginList()
        self._loginIter = {}
        self.set_rules_hint(True)
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
        self.connect('show', self.showEvent)
        self.manager.connect('state', self.stateEvent)
        self.manager.connect('contact-added', self.contactAddedEvent)
        self.manager.connect('contact-deleted', self.contactDeletedEvent)
        self.manager.connect('who', self.whoEvent)
        self.manager.connect('logout', self.logoutEvent)
        self.resetStore()

    @property
    def _listStore(self):
        return self.get_model()

    def getAtSchoolPix(self, atSchool):
        return icons.epitech if atSchool else icons.void

    def getStatePix(self, state):
        return self.pixs.get(state, icons.void)

    def resetStore(self):
        self._listStore.clear()
        self._loginIter = {}
        for login, state, atSchool in self._list.formatWatchList():
            self._loginIter[login] = self._listStore.append([
                self.getStatePix(state),
                login,
                self.getAtSchoolPix(atSchool),
                "",
            ])

    def updateLogin(self, login_name):
        login, state, atSchool = self._list.loginWatchlist(login_name)
        it = self._loginIter.get(login)
        if it is not None:
            self._listStore.set(
                it,
                0, self.getStatePix(state),
                2, self.getAtSchoolPix(atSchool)
            )

    def stateEvent(self, widget, info, state):
        self._list.changeState(info, state)
        self.updateLogin(info.login)

    def contactAddedEvent(self, widget, login):
        self._list.clean()
        self.resetStore()

    def contactDeletedEvent(self, widget, login):
        self._list.clean()
        self.resetStore()

    def whoEvent(self, widget, results):
        self._list.processWho(results)
        for login in results.logins:
            self.updateLogin(login)

    def logoutEvent(self, widget, info):
        self._list.logout(info)
        self.updateLogin(info.login)

    def rowActivated(self, tv, path, column):
        self.manager.doOpenChat(self._listStore.get_value(self._listStore.get_iter(path), self._loginColumn))

    def buttonPressEvent(self, wid, event):
        # 3 is right click
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            path = self.get_path_at_pos(int(event.x), int(event.y))
            if path is not None:
                login = self._listStore.get_value(self._listStore.get_iter(path[0]), self._loginColumn)
                menu = gtk.Menu()
                items = [
                    (gtk.STOCK_DELETE, 'Delete', self.deleteContactEvent),
                    (gtk.STOCK_FILE, 'Send file', self.sendFileEvent)
                ]
                for stock, label, call in items:
                    item = gtk.ImageMenuItem(stock_id=stock)
                    item.set_label(label)
                    item.connect("activate", call, login)
                    item.show()
                    menu.append(item)
                menu.popup(None, None, None, event.button, event.time)

    def showEvent(self, widget):
        self.grab_focus()

    def deleteContactEvent(self, widget, login):
        self.manager.doDeleteContact(login)

    def sendFileEvent(self, widget, login):
        self.downloadManager.startFileUpload(login)
