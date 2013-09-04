# -*- coding: utf-8 -*-

import os
import sys
import shutil
import logging
import platform
from argparse import ArgumentParser

from common import CptCommon


def get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose', help='Set verbose mode', default=0)
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    parser.add_argument('-d', action='store_true', dest='debug', help='Start with debug window')
    parser.add_argument('--install', action='store_true', dest='install', help='Start in install mode')
    parser.add_argument('--update_web', action='store_true', dest='update_web', help='Start in web update mode')
    parser.add_argument('--update_file', action='store', dest='update_file', help='Start in file update mode', metavar='FILE', default='', type=str)
    return parser.parse_args()


def configLogging():
    fmt = '%(levelname)s\t: %(message)s'
    level = logging.DEBUG
    if CptCommon.cmdline.verbose <= 3:
        level = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG][CptCommon.cmdline.verbose]
    logging.basicConfig(level=level, format=fmt)


def normal_mode():
    # imports
    from twisted.internet import gtk2reactor
    gtk2reactor.install()
    from twisted.internet import reactor
    from twisted.python import log
    observer = log.PythonLoggingObserver()
    observer.start()
    from config import createConfigFile
    from manager import Manager
    # start
    configLogging()
    CptCommon.config = createConfigFile()
    manager = Manager()
    manager()
    reactor.run()
    if CptCommon.willReboot:
        os.execl(sys.executable, sys.executable, *sys.argv)


def install_mode():
    if platform.system() != 'Linux':
        exit(1)

    def try_to_import(module):
        try:
            __import__(module)
            return True
        except:
            return False

    modules = filter(try_to_import, ['twisted', 'pygtk'])
    if not modules:
        print "Missing module: %s." % ', '.join(modules)
        exit(1)
    if os.getuid() == 0:
        name = os.path.dirname(os.path.abspath(__file__))
        shutil.copy(name, os.path.join('/usr/bin', 'cptsoul'))
        print "Successfully installed"
    else:
        print "You must be root/sudo in order to install."
        exit(1)


def update_file_mode(path):
    if platform.system() != 'Linux':
        exit(1)
    if os.getuid() == 0:
        shutil.copy(path, os.path.join('/usr/bin', 'cptsoul'))
        print "Successfully installed"
    else:
        print "You must be root/sudo in order to install."
        exit(3)


def update_web_mode():
    if platform.system() != 'Linux':
        exit(1)
    from urllib2 import urlopen
    if os.getuid() == 0:
        url = urlopen(CptCommon.updateUrl)
        if url.code != 200:
            print "Error while downloading"
            exit(2)
        f = file(os.path.join('/usr/bin', 'cptsoul'), 'w')
        f.write(url.read())
        f.close()
        print "Successfully installed"
    else:
        print "You must be root/sudo in order to install."
        exit(3)


def main():
    CptCommon.cmdline = get_args()
    if CptCommon.cmdline.install:
        install_mode()
    elif CptCommon.cmdline.update_web:
        update_web_mode()
    elif CptCommon.cmdline.update_file:
        update_file_mode(CptCommon.cmdline.update_file)
    else:
        normal_mode()

if __name__ == '__main__':
    main()
