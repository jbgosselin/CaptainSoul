# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def _void():
    pass


def _get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-v', '--verbose', action='count', dest='verbose', help='Set verbose mode', default=0)
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    return parser.parse_args()

options = _get_args()
