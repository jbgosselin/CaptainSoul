#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import shutil
import os


def try_to_import(module):
    try:
        __import__(module)
        return True
    except:
        return False


def main():
    modules = filter(try_to_import, ['twisted', 'pygtk'])
    if not modules:
        print "Missing module: %s." % ', '.join(modules)
        exit(1)
    if os.getuid() == 0:
        shutil.copy('./cptsoul', os.path.join('/usr/bin', 'cptsoul'))
        print "Successfully installed"
    else:
        print "You must be root/sudo in order to install."
        exit(1)


if __name__ == '__main__':
    main()
