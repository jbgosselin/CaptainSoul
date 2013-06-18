# -*- coding: utf-8 -*-

import re
import webbrowser
from time import localtime, strftime

import gtk
import webkit

from captainsoul.common import CptCommon


class ChatView(gtk.ScrolledWindow, CptCommon):
    http_regex = re.compile(r"(?P<link>https?://[\w\-\.~\:/\?#\[\]@!$&'\(\)\*\+,;=%]+)")

    def __init__(self, login, msg=None):
        super(ChatView, self).__init__()
        self.set_properties(
            border_width=0,
            shadow_type=gtk.SHADOW_ETCHED_IN,
            hscrollbar_policy=gtk.POLICY_NEVER,
            vscrollbar_policy=gtk.POLICY_AUTOMATIC
        )
        self._buffer = ""
        self._createUi()
        self.connect('destroy', self.destroyEvent)
        self._connections = [
            self.manager.connect('msg', self.msgEvent, login),
            self.manager.connect('send-msg', self.sendMsgEvent, login)
        ]
        if msg is not None:
            self.printMsg(login, msg)

    def _createUi(self):
        self._web = webkit.WebView()
        self._web.connect('navigation-policy-decision-requested', self.openLink)
        self._web.connect('size-allocate', self.scrollView)
        self.add(self._web)

    def scrollView(self, widget, alloc):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def printMsg(self, login, msg):
        self._buffer += "(%s) <b>[%s] : </b>" % (strftime("%H:%M:%S", localtime()), login)
        changes = [
            ("<", "&lt;"),
            (">", "&gt;"),
            ("\t", "&emsp;"),
            ("\n", "<br>"),
        ]
        for orig, new in changes:
            msg = re.sub(orig, new, msg)
        self._buffer += self.http_regex.sub('<a href="\g<link>">\g<link></a>', msg)
        self._buffer += "<br>"
        self._web.load_html_string(u'<html><body style="max-width:100%%;">%s</body></html>' % self._buffer , "")

    def msgEvent(self, widget, info, msg, dests, login):
        if login == info.login:
            self.printMsg(login, msg)

    def sendMsgEvent(self, widget, msg, dests, login):
        if login in dests:
            self.printMsg('Me', msg)

    def destroyEvent(self, widget):
        for co in self._connections:
            self.manager.disconnect(co)

    def openLink(self, widget, frame, request, action, policy):
        webbrowser.open_new_tab(request.get_uri())
        return True
