#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
from subprocess import check_call


def main():
    out = file('./src/icons/data.py', 'w')
    out.write('# -*- coding: utf-8 -*-\n\n\n')
    for f in os.listdir('./icons/'):
        if f.endswith('.png'):
            name = f[:-4]
            check_call(['gdk-pixbuf-pixdata', './icons/%s' % f, './icons/%s.raw' % name])
            tmp = file('./icons/%s.raw' % name, 'r')
            out.write('raw_%s = %r\n' % (name, tmp.read()))
            tmp.close()
    out.close()

if __name__ == '__main__':
    main()
