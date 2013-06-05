# -*- coding: utf-8 -*-

from gi.repository import Gtk
from twisted.internet import reactor

from CmdLine import options
from Netsoul import NsFactory
from Config import Config
import Icons

from WatchList import WatchList
from ToolBar import ToolBar
from SettingsWindow import SettingsWindow
from AddContactWindow import AddContactWindow
from Systray import Systray
from WindowManager import WindowManager


class MainWindow(Gtk.Window):
    _protocol = None

    def __init__(self):
        super(MainWindow, self).__init__(title="CaptainSoul", border_width=2, icon=Icons.shield.get_pixbuf())
        self._manager = WindowManager(self)
        self._createUi()
        self.resize(Config.mainWidth, Config.mainHeight)
        self.connect("delete-event", self.deleteEvent)
        self.connect("configure-event", self.resizeEvent)
        if Config.autoConnect:
            self.connectEvent()
        if not options.tray:
            self.show_all()

    def _createUi(self):
        self._systray = Systray(self)
        box = Gtk.VBox(False, 0)
        self._toolbar = ToolBar(self)
        box.pack_start(self._toolbar, False, False, 0)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_size_request(160, 50)
        self._watchlist = WatchList(self)
        scroll.add_with_viewport(self._watchlist)
        box.pack_start(scroll, True, True, 0)
        self._status = Gtk.Statusbar()
        box.pack_start(self._status, False, False, 0)
        self._status.push(0, "Welcome")
        self.add(box)

    # Events

    def resizeEvent(self, *args, **kwargs):
        w, h = self.get_size()
        Config.mainWidth = w
        Config.mainHeight = h

    def quitEvent(self, *args, **kwargs):
        reactor.stop()

    def deleteEvent(self, *args, **kwargs):
        self.set_visible(False)
        return True

    def connectEvent(self, *args, **kwargs):
        self._toolbar.connectEvent()
        self._status.push(0, "Connecting")
        self.createConnection()

    def disconnectEvent(self, *args, **kwargs):
        self._toolbar.disconnectEvent()
        self.stopConnection()

    def settingsEvent(self, *args, **kwargs):
        SettingsWindow().destroy()

    def showHideEvent(self, *args, **kwargs):
        if self.get_visible():
            self.set_visible(False)
        else:
            self.show_all()
            self.set_visible(True)

    def addContactWindowEvent(self, *args, **kwargs):
        AddContactWindow(self).destroy()
        self.sendWatch()

    # Senders

    def sendState(self, state):
        if self._protocol is not None:
            self._protocol.sendState(state)

    def sendWatch(self):
        if self._protocol is not None:
            self._protocol.sendWatch()

    def sendMsg(self, msg, dests):
        if self._protocol is not None:
            self._protocol.sendMsg(msg, dests)

    def sendWho(self, logins):
        if self._protocol is not None:
            self._protocol.sendWho(logins)

    def sendExit(self):
        if self._protocol is not None:
            self._protocol.sendExit()

    def sendStartTyping(self, dests):
        if self._protocol is not None:
            self._protocol.sendStartTyping(dests)

    def sendCancelTyping(self, dests):
        if self._protocol is not None:
            self._protocol.sendCancelTyping(dests)

    # Netsoul Actions

    def createConnection(self):
        if self._protocol is not None:
            self.stopConnection()
        reactor.connectTCP("ns-server.epita.fr", 4242, NsFactory(self))

    def stopConnection(self):
        if self._protocol is not None:
            self.sendExit()
            self._protocol.transport.loseConnection()

    # Netsoul Hooks

    def setProtocol(self, protocol):
        self._protocol = protocol

    def loggedHook(self):
        self._status.push(0, "Connected")

    def loginFailedHook(self):
        self.disconnectEvent()

    def connectionLostHook(self):
        self._protocol = None
        self._status.push(0, "Disconnected")

    def connectionMadeHook(self):
        pass

    def cmdStateHook(self, info, state):
        self._watchlist.setState(info.login, state)
        self._manager.changeState(info.login, state)

    def cmdLoginHook(self, info):
        self._manager.changeState(info.login, 'login')

    def cmdLogoutHook(self, info):
        self._watchlist.setState(info.login, 'logout')
        self._manager.changeState(info.login, 'logout')

    def cmdIsTypingHook(self, info):
        self._manager.startTyping(info.login)

    def cmdCancelTypingHook(self, info):
        self._manager.cancelTyping(info.login)

    def cmdMsgHook(self, info, msg, dest):
        self._systray.notifyMessage(info.login, msg)
        self._manager.showMsg(info.login, msg)

    def cmdWhoHook(self, result):
        for res in result:
            self._watchlist.setState(res.login, res.state)
            self._manager.changeState(res.login, res.state)
