# -*- coding: utf-8 -*-

from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.python import log
observer = log.PythonLoggingObserver()
observer.start()

import logging
import platform
from argparse import ArgumentParser
from common import CptCommon


def get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose', help='Set verbose mode', default=0)
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    parser.add_argument('-d', action='store_true', dest='debug', help='Start with debug window')
    return parser.parse_args()
CptCommon.cmdline = get_args()


def configLogging():
    fmt = '%(levelname)s\t: %(message)s'
    level = logging.WARNING
    if CptCommon.cmdline.verbose >= 2:
        level = logging.DEBUG
    elif CptCommon.cmdline.verbose == 1:
        level = logging.INFO
    logging.basicConfig(level=level, format=fmt)
configLogging()

from config import createConfigFile
CptCommon.config = createConfigFile()

if platform.system() == 'Linux':
    try:
        import pynotify
        pynotify.init("CaptainSoul")
    except ImportError:
        logging.warning('Init : pynotify is not installed')

from manager import Manager


def main():
    manager = Manager()
    manager()
    reactor.run()

if __name__ == '__main__':
    main()
