"""
The daemon takes care of creating screenshots and log entries
"""

import os
import signal
import sys
import argparse

from multiprocessing import Process

from . import monitor
from . import webserver
from . import external_dependencies

NO_SIGNAL_CAUGHT = 0

"""Interval between periodic screenshots expiries: once a day"""
SCREENSHOTS_EXPIRY_INTERVAL = 24 * 60 * 60

long_help = """The daemon runs in the backgound. It monitors the users
activity (and creates screenshots) and it provides a web server for the web user
interface. You can also start the monitor and web server separately.
"""


def add_parser(subparsers):
    help = "Run forever recoring desktop environment activity"

    parser = subparsers.add_parser(
        'daemon',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help=help,
        description=long_help)

    parser.add_argument(
        '--monitor-start-only',
        action='store_const',
        default=False,
        const=True,
        help="Only start the monitor")

    parser.add_argument(
        '--web-server-start-only',
        action='store_const',
        default=False,
        const=True,
        help="Only start the web server")

    parser.add_argument(
        '--dev-web-server-start-only',
        action='store_const',
        default=False,
        const=True,
        help="""Only start the web server but in development mode, with hot
             reloading and CORS disabled. This is not intended for production
             use.""")

    parser.add_argument(
        '--log-output-to-files',
        action='store_const',
        default=False,
        const=True,
        help="""Store output from monitor and webserver in separate log files
             under storage if running them both (without any of the
             --*-start-only flags)""")

    monitor_group_parser = parser.add_argument_group(
        'activity monitor options')
    monitor.add_parser_arguments(monitor_group_parser)

    webserver_group_parser = parser.add_argument_group(
        'web server options')
    webserver.add_parser_arguments(webserver_group_parser)

    parser.set_defaults(func=subcommand, config_key='daemon')


def run_process(target, args, logname):
    if args.log_output_to_files:
        with open(args.under_storage(logname + ".log"), 'a+') as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())
            target(args)
    else:
        target(args)

def start_all(args):
    print('starting all: webserver and monitor')

    webserver_process = Process(
        name="webserver",
        target=run_process,
        args=(webserver.run_webserver, args, 'webserver'),
    )
    webserver_process.start()

    monitor_process = Process(
        name="monitor",
        target=run_process,
        args=(monitor.run_monitor, args, 'monitor'),
    )
    monitor_process.start()

    processes = set()
    processes.add(webserver_process)
    processes.add(monitor_process)

    for p in processes:
        print(f'    Started {p.name} pid {p.pid}')

    while len(processes):
        pid, _ = os.wait()
        done_process = next(filter(lambda p: p.pid == pid, processes))
        print(f"done: {done_process.name}/{done_process.pid}")
        processes.discard(done_process)
        # When one of them has finished, kill the others
        for p in processes:
            print(f'killing {p.name}/{p.pid}')
            os.kill(p.pid, signal.SIGTERM)

    webserver_process.join()
    monitor_process.join()


def subcommand(args):
    if not args.show_detections:
        external_dependencies.check_dependencies(args)

    should_start_all = not (
        monitor.handles(args) or
        args.web_server_start_only or
        args.dev_web_server_start_only)
    if should_start_all:
        start_all(args)
        sys.exit(0)

    if monitor.handles(args):
        monitor.run_monitor(args)
        sys.exit(0)

    if args.web_server_start_only:
        webserver.run_webserver(args)
        sys.exit(0)

    if args.dev_web_server_start_only:
        webserver.run_webserver(args, dev_mode=True)
        sys.exit(0)

    raise RuntimeError("An action should've been performed by now")
