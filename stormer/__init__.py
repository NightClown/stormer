__version__ = '0.1.0'

import sys
import argparse
from stormer.logger import logger
from stormer.locust import LocustStarter
from stormer import ssh

def main():
    """ parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(
        description='Wrappers for making load test with locust more convienient.')

    subparsers = parser.add_subparsers(help='sub-command help')

    locust_subparser = subparsers.add_parser(
        'locust', help='locust wrapper.',
        description='Start locust master and specified number of slaves with one command.')
    locust_subparser.add_argument(
        '-f', '--locustfile', help="Specify locust file to run test.")
    locust_subparser.add_argument(
        '-P', '--port', '--web-port', default=8089, type=int,
        help="Port on which to run web host, default is 8089.")
    locust_subparser.add_argument(
        '--slave-only', action='store_true',
        help="Only start locust slaves.")
    locust_subparser.add_argument(
        '--master-host', default='127.0.0.1',
        help="Host or IP address of locust master for distributed load testing.")
    locust_subparser.add_argument(
        '--slaves-num', type=int,
        help="Specify number of locust slaves, default to machine's cpu count.")
    locust_subparser.set_defaults(func=main_locust)

    sput_subparser = subparsers.add_parser(
        'sput', help='scp wrapper for putting files.',
        description='Copy local file/directory to remote machines and overwrite.')
    sput_subparser.add_argument(
        '--hostsfile', help="Specify hosts file to handle.")
    sput_subparser.add_argument(
        '--localpath', help="Specify localpath of file or directory to transfer.")
    sput_subparser.add_argument(
        '--remotepath', help="Specify remotepath of file or directory to transfer.")
    sput_subparser.set_defaults(func=main_sput)

    args = parser.parse_args()
    args.func(args)

def main_locust(args):
    locustfile = args.locustfile
    if not locustfile:
        logger.error("locustfile must be specified! use the -f option.")
        sys.exit(0)

    LocustStarter(args.master_host, args.port, args.slave_only).start(
        args.locustfile,
        args.slaves_num
    )

def main_sput(args):
    hostsfile = args.hostsfile
    if not hostsfile:
        logger.error("hostsfile must be specified! use the --hostsfile option.")
        sys.exit(0)

    localpath = args.localpath
    if not localpath:
        logger.error("localpath must be specified! use the --localpath option.")
        sys.exit(0)

    ssh.sput(hostsfile, localpath, args.remotepath)
