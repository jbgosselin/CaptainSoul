#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="CaptainSoul",
    version="0.1.2",
    author="gossel_j",
    author_email="***REMOVED***",
    description="Netsoul client with pygtk and twisted",
    url="https://github.com/gossel-j/CaptainSoul",
    packages=find_packages(),
    zip_safe=True,
    entry_points={
        'gui_scripts': [
            'cptsoul = cptsoul.entry_points:cptsoul'
        ]
    },
    install_requires=[
    ],
    package_data={
        'cptsoul': ['icons/*.png']
    }
)
