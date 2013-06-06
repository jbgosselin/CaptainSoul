# -*- coding: utf-8 -*-

import logging
from time import time
from hashlib import md5
from collections import deque

from twisted.protocols.basic import LineOnlyReceiver

from ..Config import Config
from NetsoulTools import Rea, ReaList, NsData, NsUserCmdInfo, NsWhoResult, NsWhoEntry, urlEncode, urlDecode

__all__ = ['NsProtocol']


class NsProtocol(LineOnlyReceiver, object):
    delimiter = '\n'
    _response_queue = deque()
    _who_queue = deque()

    def __init__(self, factory):
        self.factory = factory
        self.factory.setProtocol(self)
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
            Rea(r'^state (?P<state>\w+?)(:\d+)?\s?$', self._cmdStateHook),
            Rea(r'^login\s?$', self._cmdLoginHook),
            Rea(r'^logout\s?$', self._cmdLogoutHook),
            Rea(r'^dotnetSoul_UserTyping null dst=.*$', self._cmdIsTypingHook),
            Rea(r'^dotnetSoul_UserCancelledTyping null dst=.*$', self._cmdCancelTypingHook))

    def lineReceived(self, line):
        logging.debug('Netsoul : <<   : "%s"' % line)
        if not self._realist.found_match(line):
            logging.warning('Netsoul : Unknown line : "%s"' % line)

    def connectionLost(self, reason):
        pass

    def connectionMade(self):
        self.factory.connectionMadeHook()

    def sendLine(self, line):
        super(NsProtocol, self).sendLine(str(line))
        logging.debug('Netsoul :   >> : "%s"' % line)

    # HOOKS

    def _userCmdHook(self, no, login, ip, loc, cmd):
        if not self._cmd_realist.found_match_cmd(cmd, NsUserCmdInfo(int(no), login, ip, loc)):
            logging.warning('Netsoul : Unknown cmd from %s@%s : "%s"' % (login, ip, cmd))

    def _responseHook(self, no):
        no = int(no)
        if self._response_queue:
            logging.info('Netsoul : Got response %d' % no)
            self._response_queue.popleft()(no)
        else:
            logging.warning('Netsoul : No response expected')

    def _pingHook(self, t):
        logging.info('Netsoul : Got ping %d' % int(t))
        self.sendLine('ping %s' % t)

    def _salutHook(self, num, md5_hash, ip, port, timestamp):
        logging.info('Netsoul : Got salut %s %s:%s' % (md5_hash, ip, port))
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
            self.factory.cmdWhoHook(self._who_queue.popleft())
        else:
            logging.warning("Netsoul : No who expected")

    def _cmdMsgHook(self, info, msg, dest):
        self.factory.cmdMsgHook(info, urlDecode(msg), dest.split(','))

    def _cmdLoginHook(self, info):
        self.factory.cmdLoginHook(info)

    def _cmdLogoutHook(self, info):
        self.factory.cmdLogoutHook(info)

    def _cmdStateHook(self, info, state):
        self.factory.cmdStateHook(info, state)

    def _cmdIsTypingHook(self, info):
        self.factory.cmdIsTypingHook(info)

    def _cmdCancelTypingHook(self, info):
        self.factory.cmdCancelTypingHook(info)

    # RESPONSE HOOKS

    def _responseSalutHook(self, no):
        if no == 2:
            md5_hash = md5('%s-%s/%s%s' % (self._info.hash, self._info.host, self._info.port, Config['password'])).hexdigest()
            self.sendLine('ext_user_log %s %s %s %s' % (Config['login'], md5_hash, urlEncode(Config['location']), 'CaptainSoul'))
            self._response_queue.append(self._responseLogHook)
        else:
            logging.warning('Netsoul : Salut response unknown %d' % no)

    def _responseLogHook(self, no):
        if no == 2:
            self.factory.loggedHook()
        elif no == 33:
            self.factory.loginFailedHook()
        elif no == 131:
            # permission denied
            self.factory.loginFailedHook()
        else:
            logging.warning('Netsoul : Log response unknown %d' % no)
            self.factory.loginFailedHook()

    # COMMANDS

    def sendState(self, state):
        if state:
            self.sendLine('state %s:%d' % (state, time()))

    def sendWatch(self, sendWho=True):
        self.sendLine('user_cmd watch_log_user {%s}' % ','.join(Config['watchlist']))
        if sendWho:
            self.sendWho(Config['watchlist'])

    def sendMsg(self, msg, dests):
        if msg and dests:
            self.sendLine('user_cmd msg_user {%s} msg %s' % (','.join(dests), urlEncode(msg)))

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
