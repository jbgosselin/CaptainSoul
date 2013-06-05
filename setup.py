#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name="CaptainSoul",
    version="0.1",
    description="Netsoul client with twisted and gtk3",
    author="gossel_j",
    author_email="jbgosselin@gmail.com",
    url="https://github.com/gossel-j/captain-soul",
    packages=["captainsoul"],
    package_data={"captainsoul": ["Icons/*"]},
    scripts=["cptsoul"]
)
