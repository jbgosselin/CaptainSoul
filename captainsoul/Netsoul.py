# -*- coding: utf-8 -*-

import logging
from time import time
from hashlib import md5
from urllib import quote as urlquote
from urllib import unquote as urlunquote
from collections import deque

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver

from Config import Config
from NetsoulTools import Rea, ReaList, NsData, NsUserCmdInfo, NsWhoResult, NsWhoEntry

__all__ = ['NsProtocol', 'NsFactory']


class NsProtocol(LineOnlyReceiver, object):
    delimiter = '\n'
    _response_queue = deque()
    _who_queue = deque()

    def __init__(self, hooker):
        self._hooker = hooker
        self._hooker.setProtocol(self)
        self._info = NsData()
        self._realist = ReaList(
            Rea(r'^rep (?P<no>\d+) -- .*$', self._responseHook),
            Rea(r'^ping (?P<t>\d+)\s?$', self._pingHook),
            Rea(r'^salut (?P<num>\d+) (?P<md5_hash>[0-9a-fA-F]{32}) (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                ' (?P<port>\d{1,5}) (?P<timestamp>\d+)$', self._salutHook),
            Rea(r'^user_cmd (?P<no>\d+):\w+:\d+/\d+:(?P<login>.+)@(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                ':.+:(?P<loc>.+):.+ \| (?P<cmd>.*)$', self._userCmdHook))
        self._cmd_realist = ReaList(
            Rea(r'^who (?P<no>\d+) (?P<login>.+) (?P<ip>[\d\.]{7,15}) \d+ \d+ \d+ \d+ .+ (?P<loc>.+) .+ (?P<state>\w+)(:\d+)? (?P<res>.+)$', self._cmdWhoHook),
            Rea(r'^who rep 002 -- cmd end$', self._cmdWhoEndHook),
            Rea(r'^msg (?P<msg>.+) dst=(?P<dest>.*)$', self._cmdMsgHook),
            Rea(r'^state (?P<state>\w+?)(:\d+)?\s?$', self._hooker.cmdStateHook),
            Rea(r'^login\s?$', self._cmdLoginHook),
            Rea(r'^logout\s?$', self._cmdLogoutHook),
            Rea(r'^dotnetSoul_UserTyping null dst=.*$', self._hooker.cmdIsTypingHook),
            Rea(r'^dotnetSoul_UserCancelledTyping null dst=.*$', self._hooker.cmdCancelTypingHook))

    def lineReceived(self, line):
        logging.info('Netsoul : <<   : "%s"' % line)
        if not self._realist.found_match(line):
            logging.warning('Netsoul : Unknown line : "%s"' % line)

    def connectionLost(self, reason):
        logging.info('Netsoul : Connection Lost')
        self._hooker.connectionLostHook()

    def connectionMade(self):
        logging.info('Netsoul : Connection Made')
        self._hooker.connectionMadeHook()

    def sendLine(self, line):
        super(NsProtocol, self).sendLine(str(line))
        logging.info('Netsoul :   >> : "%s"' % line)

    # HOOKS

    def _userCmdHook(self, no, login, ip, loc, cmd):
        if not self._cmd_realist.found_match_cmd(cmd, NsUserCmdInfo(int(no), login, ip, loc)):
            logging.warning('Netsoul : Unknown cmd from %s@%s : "%s"' % (login, ip, cmd))

    def _responseHook(self, no):
        no = int(no)
        logging.debug('Netsoul : Got response %d' % no)
        if self._response_queue:
            self._response_queue.popleft()(no)
        else:
            logging.warning('Netsoul : No response expected')

    def _pingHook(self, t):
        logging.debug('Netsoul : Got ping %d' % int(t))
        self.sendLine('ping %s' % t)

    def _salutHook(self, num, md5_hash, ip, port, timestamp):
        logging.debug('Netsoul : Got salut %s %s:%s' % (md5_hash, ip, port))
        self._info.hash = md5_hash
        self._info.host = ip
        self._info.port = port
        self.sendLine('auth_ag ext_user none none')
        self._response_queue.append(self._responseSalutHook)

    # CMD HOOKS

    def _cmdWhoHook(self, info, no, login, ip, loc, state, res):
        if self._who_queue:
            self._who_queue[0].add(NsWhoEntry(no, login, ip, loc, state, res))
        else:
            logging.warning("Netsoul : No who expected")

    def _cmdWhoEndHook(self, info):
        if self._who_queue:
            self._hooker.cmdWhoHook(self._who_queue.popleft())
        else:
            logging.warning("Netsoul : No who expected")

    def _cmdMsgHook(self, info, msg, dest):
        msg = urlunquote(msg)
        dest = dest.split(',')
        logging.debug('Netsoul : Got Msg %s "%s" %s' % (info, msg, dest))
        self._hooker.cmdMsgHook(info, msg, dest)

    def _cmdLoginHook(self, info):
        logging.debug('Netsoul : Got Login %s' % info)
        self._hooker.cmdLoginHook(info)
        self.sendWho([info.login])

    def _cmdLogoutHook(self, info):
        logging.debug('Netsoul : Got Logout %s' % info)
        self._hooker.cmdLogoutHook(info)

    # RESPONSE HOOKS

    def _responseSalutHook(self, no):
        if no == 2:
            md5_hash = md5('%s-%s/%s%s' % (self._info.hash, self._info.host, self._info.port, Config['password'])).hexdigest()
            self.sendLine('ext_user_log %s %s %s %s' % (Config['login'], md5_hash, urlquote(Config['location']), 'CaptainSoul'))
            self._response_queue.append(self._responseLogHook)
        else:
            logging.warning('Netsoul : Salut response unknown %d' % no)

    def _responseLogHook(self, no):
        if no == 2:
            logging.debug('Netsoul : Logged')
            self.sendState('actif')
            self.sendWatch()
            self._hooker.loggedHook()
        elif no == 33:
            logging.debug('Netsoul : Login failed')
            self._hooker.loginFailedHook()
        elif no == 131:
            # permission denied
            logging.debug('Netsoul : Login failed')
            self._hooker.loginFailedHook()
        else:
            logging.warning('Netsoul : Log response unknown %d' % no)

    # COMMANDS

    def sendState(self, state):
        if state:
            self.sendLine('state %s:%d' % (state, time()))

    def sendWatch(self):
        self.sendLine('user_cmd watch_log_user {%s}' % ','.join(Config['watchlist']))
        self.sendWho(Config['watchlist'])

    def sendMsg(self, msg, dests):
        if msg and dests:
            self.sendLine('user_cmd msg_user {%s} msg %s' % (','.join(dests), urlquote(msg)))

    def sendWho(self, logins):
        if logins:
            self._who_queue.append(NsWhoResult(logins))
            self.sendLine('user_cmd who {%s}' % ','.join(logins))

    def sendExit(self):
        self.sendLine('exit')

    def sendStartTyping(self, dests):
        self.sendLine('user_cmd msg_user {%s} dotnetSoul_UserTyping null' % ','.join(dests))

    def sendCancelTyping(self, dests):
        self.sendLine('user_cmd msg_user {%s} dotnetSoul_UserCancelledTyping null' % ','.join(dests))


class NsFactory(ClientFactory):
    def __init__(self, hooker):
        self._hooker = hooker

    def buildProtocol(self, addr):
        return NsProtocol(self._hooker)

    def clientConnectionFailed(self, connector, reason):
        logging.warning('Netsoul : Connection failed reconnecting')
        reactor.callLater(3, connector.connect)
