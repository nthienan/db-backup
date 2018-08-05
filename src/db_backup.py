#!/usr/bin/env python

import argparse
import signal
import sys

from db.backup.app import Application


# from db_backup.app import Application


def parse_opts(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-file', dest='cfg_file',
                        help='config file')
    return parser.parse_args(args)


def sigterm_handler(signum, frame):
    if application and signal.SIGTERM == signum:
        application.stop()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, sigterm_handler)
    opts = parse_opts(sys.argv[1:])
    application = Application(opts.cfg_file)
    sys.exit(application.run())
