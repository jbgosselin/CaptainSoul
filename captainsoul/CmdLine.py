# -*- coding: utf-8 -*-

from argparse import ArgumentParser


def _void():
    pass


def _get_args():
    parser = ArgumentParser(prog='cptsoul')
    parser.add_argument('-dd', action='store_true', dest='log_debug', help='Set debug mode')
    parser.add_argument('-d', action='store_true', dest='log_info', help='Set info mode')
    parser.add_argument('-t', action='store_true', dest='tray', help='Start in tray')
    return parser.parse_args()

options = _get_args()
