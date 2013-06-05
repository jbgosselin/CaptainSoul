# -*- coding: utf-8 -*-

import re
from urllib import unquote as urlunquote


__all__ = ['Rea', 'ReaList', 'NsUserCmdInfo', 'NsData', 'NsWhoEntry', 'NsWhoResult']


class Rea(object):
    def __init__(self, regex, f):
        self._regex = re.compile(regex)
        self._f = f

    def try_call(self, entry):
        m = self._regex.match(entry)
        if m is not None and self._f is not None:
            self._f(**m.groupdict())
            return True
        return False

    def try_call_cmd(self, entry, info):
        m = self._regex.match(entry)
        if m is not None and self._f is not None:
            self._f(info, **m.groupdict())
            return True
        return False


class ReaList(object):
    def __init__(self, *args):
        self._reas = [rea for rea in args if isinstance(rea, Rea)]

    def found_match(self, entry):
        for m in self._reas:
            if m.try_call(entry):
                return True
        return False

    def found_match_cmd(self, entry, info):
        for m in self._reas:
            if m.try_call_cmd(entry, info):
                return True
        return False


class NsUserCmdInfo(object):
    def __init__(self, login, ip, location):
        self._login = login
        self._ip = ip
        self._location = urlunquote(location)

    def __str__(self):
        return '<%s@%s "%s">' % (self.login, self.ip, self.location)

    @property
    def login(self):
        return self._login

    @property
    def ip(self):
        return self._ip

    @property
    def location(self):
        return self._location


class NsData(object):
    _hash = ''
    _host = ''
    _port = 0

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, v):
        self._hash = v

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, v):
        self._host = v

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, v):
        self._port = v


class NsWhoEntry(object):
    def __init__(self, login, ip, location, state, res):
        self._login = login
        self._ip = ip
        self._location = location
        self._state = state
        self._res = res

    @property
    def login(self):
        return self._login

    @property
    def ip(self):
        return self._ip

    @property
    def location(self):
        return self._location

    @property
    def state(self):
        return self._state

    @property
    def res(self):
        return self._res


class NsWhoResult(object):
    def __init__(self, logins):
        self._logins = logins
        self._list = []

    @property
    def logins(self):
        return self._logins

    def add(self, entry):
        self._list.append(entry)

    def __iter__(self):
        return iter(self._list)
