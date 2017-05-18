# -*- coding: utf-8 -*-

from cptsoul.common import CptCommon


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

    @property
    def atSchool(self):
        return self._ip.startswith('10.')

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<Buddy %d %s %s %s "%s">' % (self.no, self.login, self.state, self.ip, self.location)


class LoginList(CptCommon):
    def __init__(self):
        self._list = {}

    def clean(self):
        self._list = {no: buddy for no, buddy in self._list.iteritems() if buddy.login in self.config['watchlist']}

    def processWho(self, results):
        self._list = {no: b for no, b in self._list.iteritems() if b.login not in results.logins}
        for r in results:
            if r.login in self.config['watchlist']:
                self._list[r.no] = Buddy(r.no, r.login, r.state, r.ip, r.location)

    def formatWatchList(self):
        return [self.loginWatchlist(login) for login in self.config['watchlist']]

    def loginWatchlist(self, login):
        return login, self.getState(login), self.atSchool(login)

    def getFromLogin(self, login):
        return [buddy for buddy in self._list.itervalues() if buddy.login == login]

    def getState(self, login):
        state = 'logout'
        for buddy in self.getFromLogin(login):
            if state == 'logout' and buddy.state in ('away', 'lock', 'actif') or state in ('away', 'lock') and buddy.state == 'actif':
                state = buddy.state
        return state

    def atSchool(self, login):
        return any([buddy.atSchool for buddy in self.getFromLogin(login)])

    def changeState(self, info, state):
        if info.login in self.config['watchlist']:
            if info.no in self._list:
                self._list[info.no].state = state
            else:
                self._list[info.no] = Buddy(info.no, info.login, state, info.ip, info.location)

    def logout(self, info):
        if info.no in self._list:
            del self._list[info.no]
