# -*- coding: utf-8 -*-

from ChatWindow import ChatWindow


class WindowManager(object):
    _windows = {}

    def __init__(self, mw):
        self._mw = mw

    def openWindow(self, login):
        if login:
            if login not in self._windows:
                self._windows[login] = ChatWindow(self, self._mw, login, False)
            self._windows[login].present()

    def closeWindow(self, window, event, login):
        if login and login in self._windows:
            self._windows[login].destroy()
            del self._windows[login]
        return True

    def showMsg(self, login, msg):
        if login:
            if login not in self._windows:
                self._windows[login] = ChatWindow(self, self._mw, login, not self._mw.get_visible())
            self._windows[login].addMsg(msg)

    def changeState(self, login, state):
        if login and login in self._windows:
            self._windows[login].changeState(state)

    def startTyping(self, login):
        if login and login in self._windows:
            self._windows[login].startTyping()

    def cancelTyping(self, login):
        if login and login in self._windows:
            self._windows[login].cancelTyping()
