# -*- coding: utf-8 -*-

import gtk

from ..GetFile import FileGetter
from ..PreparedCaller import PreparedCaller
from tools import sizeFormatter, strRandom

COLUMN_NAME, COLUMN_SIZE, COLUMN_LOGIN, COLUMN_STATE, COLUMN_PROGRESS = range(5)


class DownloadList(gtk.TreeView):
    def __init__(self, downmanager, manager):
        super(DownloadList, self).__init__(model=gtk.ListStore(str, str, str, str, int))
        self.set_rules_hint(True)
        self._data = {}
        self._manager, self._downmanager = manager, downmanager
        columns = [
            gtk.TreeViewColumn("Name", gtk.CellRendererText(), text=COLUMN_NAME),
            gtk.TreeViewColumn("Size", gtk.CellRendererText(), text=COLUMN_SIZE),
            gtk.TreeViewColumn("Login", gtk.CellRendererText(), text=COLUMN_LOGIN),
            gtk.TreeViewColumn("State", gtk.CellRendererProgress(), text=COLUMN_STATE, value=COLUMN_PROGRESS),
        ]
        for column in columns:
            self.append_column(column)

    @property
    def _listStore(self):
        return self.get_model()

    def startFileTransfer(self, info, name, size, path):
        key = strRandom()
        while key in self._data:
            key = strRandom()
        self._data[key] = self._listStore.append([name, sizeFormatter(size), info.login, 'Waiting', 0])
        FileGetter(
            self._manager, info, name, path, size,
            PreparedCaller(self.progressCallback, key=key),
            PreparedCaller(self.endCallback, key=key),
            PreparedCaller(self.errorCallback, key=key)
        )
        self._downmanager.show_all()

    def progressCallback(self, done, total, key):
        if key in self._data:
            self._listStore[self._data[key]][COLUMN_STATE] = 'Downloading'
            self._listStore[self._data[key]][COLUMN_PROGRESS] = (100 * done) / total

    def endCallback(self, key):
        if key in self._data:
            self._listStore[self._data[key]][COLUMN_STATE] = 'Finished'
            self._listStore[self._data[key]][COLUMN_PROGRESS] = 100

    def errorCallback(self, key):
        if key in self._data:
            self._listStore[self._data[key]][COLUMN_STATE] = 'Error'
