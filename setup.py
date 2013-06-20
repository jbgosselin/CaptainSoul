#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from distutils.core import setup


def createPackages():
    pack = "captainsoul"
    mods = ["chatwindow", "config", "Icons", "mainwindow", "netsoul", 'debugwindow', 'getfile', 'sendfile', 'downloadmanager']
    return [pack] + ["%s.%s" % (pack, mod) for mod in mods]


setup(
    name="CaptainSoul",
    description="Netsoul client with twisted and gtk3",
    author="gossel_j",
    author_email="jbgosselin@gmail.com",
    url="https://github.com/gossel-j/captain-soul",
    packages=createPackages(),
    package_data={"captainsoul": ["Icons/*"]},
    scripts=["cptsoul"]
)
