# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def _void():
    pass


def _get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='Set debug mode')
    parser.add_argument('-t', '--tray', action='store_true', dest='tray', help='Start in tray')
    return parser.parse_args()

options = _get_args()
