"""
The daemon takes care of creating screenshots and log entries
"""

import os
import signal
import time
import sys
import pidfile
import time
import traceback

from threading import Event

from . import activity_logger
from . import constants
from . import activedetector
from . import screenshots
from . import external_dependencies
from . import database

NO_SIGNAL_CAUGHT = 0

"""Interval between periodic screenshots expiries: once a day"""
SCREENSHOTS_EXPIRY_INTERVAL = 24 * 60 * 60


def add_parser_arguments(parser):
    parser.add_argument(
        '--inactivity-poll-interval',
        type=int,
        default=10,
        metavar="SECONDS",
        help="Seconds between polls for inactivity.")

    parser.add_argument(
        '--screenshot-metadata-generator',
        metavar="PYFILE",
        default=os.path.join(constants.root_storage_dir,
                             "screenshot_metadata.py"),
        help="""\
          A python file that generates metadata for screenshots.
          It must contain a python function `def metadata():`
          that returns a dict that will be saved as
          `$image.metadata` as json.
          """)

    parser.add_argument(
        '--screenshot-interval',
        metavar="MINUTES",
        type=int,
        default=15,
        help="Minutes between screenshots")

    parser.add_argument(
        '--screenshot-now',
        action='store_const',
        const=True,
        help="Take a screenshot now and exit")

    parser.add_argument(
        '--screenshots-expiry',
        metavar="DAYS",
        type=int,
        default=15,
        help="""Expire (delete) screenshots taken this many days ago. Use 0 to
            disable expiry altogether""")

    parser.add_argument(
        '--screenshots-expire-now',
        action='store_const',
        const=True,
        help="Expire screenshots now and exit")

    parser.add_argument(
        '--show-detections',
        action='store_const',
        const=True,
        help="Show the status of the external dependencies and activity detectors "
             "now and exit"
    )

    parser.add_argument(
        '--active-detector',
        metavar="PYFILE",
        default=os.path.join(constants.root_storage_dir,
                             "detect_active.py"),
        help="""
          A python file that contains a `def
          detect_screensaver():` that returns True or False depending on whether
          the screensaver is active or None if the detection is not possible.
          """)

    parser.add_argument(
        '--screensaver-executable',
        metavar="EXECUTABLE",
        type=str,
        default=None,
        help="""To support environments where the screensaver cannot be detected
             with dbus, the name of the screensaver executable can be provided
             to detect whether the screensaver is active by looking through the
             process list to see if it appears as a substring. E.g. use
             `xfce4-screensaver` under XFCE for the standard screensaver. Check
             that it works with --show-detections when the screensaver is both
             active and inactive.""")

    parser.add_argument(
        '--no-screensaver-detection',
        action='store_const',
        const=True,
        default=False,
        help="""Whether to try to detect the screensaver as the activity
          signal. Current only supported on GNOME. (True means don't detect the
          screensaver).""")

    parser.add_argument(
        '--inactivity-time',
        type=int,
        default=5,
        metavar="MINUTES",
        help="""\
          Minutes before declaring the user inactive.
          (Ignored if we can detect the screen saver.
          Otherwise We recommend to keep this in sync
          with your screensaver config. See the README)""")


detector_exception_message = """\
Couldn't find a user active detector

We encoutered these problems when trying to find an active detector.
Please fix the problems for at least one of the active detectors.

%s"""


class ActivityState:
    def __init__(self, logger, args):
        self.inactivity_seconds = args.inactivity_time * 60
        self.args = args
        self.last_activity_loop = None
        self.logger = logger
        self.is_active = None
        detectors = activedetector.probe_detectors(args)
        self.active_detector = activedetector.find_detector(detectors)
        if self.active_detector == None:
            raise RuntimeError(
                detector_exception_message %
                (activedetector.detectors_status_string(detectors)))

    def _set_activity_state(self, state, t_log):
        if self.is_active == None or state != self.is_active:
            self.is_active = state
            if self.is_active:
                self.logger.log("active", t_log=t_log)
            else:
                self.logger.log("inactive", t_log=t_log)

    def loop(self):
        now = time.time()
        # If this was a laptop that got suspended, it will appear as if the user
        # has been active the entire time, but there has been e.g. 4 hours
        # between loops/polls. Detect and handle that.
        if self.last_activity_loop != None and \
                now - self.last_activity_loop > 2 * self.inactivity_seconds:
            self._set_activity_state(
                False, self.last_activity_loop + self.inactivity_seconds)
        self.last_activity_loop = now

        new_activity_state = None
        try:
            new_activity_state = self.active_detector.is_active()
        except Exception:
            print(traceback.format_exc())
        if new_activity_state != None:
            self._set_activity_state(new_activity_state, now)


class ScreenshotHandler:
    def __init__(self, args):
        self.screenshot_interval = args.screenshot_interval
        self.screenshots_expiry = args.screenshots_expiry
        self.last_screenshot = 0
        self.last_screenshots_expiry = 0
        generator_path = os.path.expanduser(
            args.screenshot_metadata_generator
        )

        screenshots_dir = args.under_storage('screenshots')
        self.screenshotter = screenshots.Screenshotter(
            screenshots_dir, generator_path)
        self.screenshot_consumer = screenshots.Consumer(screenshots_dir)

    def screenshot_now(self):
        return self.screenshotter.screenshot_now()

    def screenshots_expire_now(self):
        if self.screenshots_expiry == 0:
            return
        before = time.time() - 24*60*60 * self.screenshots_expiry
        # import datetime
        # print(before, datetime.datetime.fromtimestamp(before))
        self.screenshot_consumer.expire(before)

    def loop(self):
        now = time.time()
        if now - self.last_screenshot > self.screenshot_interval * 60:
            self.screenshot_now()
            self.last_screenshot = now
        if now - self.last_screenshots_expiry > SCREENSHOTS_EXPIRY_INTERVAL:
            self.screenshots_expire_now()
            self.last_screenshots_expiry = now


class Daemon:
    def __init__(self, args):
        self.args = args
        self.dbfile = args.under_storage('actlog.db')
        self.logger = activity_logger.Logger(self.dbfile)

        self.activity_state = ActivityState(self.logger, args)
        self.screenshot_handler = ScreenshotHandler(args)

        # Using an Event() is better than time.sleep() since it can be
        # interrupted by a signal handler
        self.exit_event = Event()

        self.caught_signal = NO_SIGNAL_CAUGHT
        signal.signal(signal.SIGINT, self.catch_sig)
        signal.signal(signal.SIGTERM, self.catch_sig)

    def catch_sig(self, signal_number, stack_frame):
        self.caught_signal = signal_number
        self.exit_event.set()

    def uncaught_loop_forever(self):
        """
        uncaught_loop_forever runs a loop forever, but may raise exceptions
        """
        while True:
            self.activity_state.loop()
            if self.activity_state.is_active:
                self.screenshot_handler.loop()

            self.exit_event.wait(self.args.inactivity_poll_interval)
            if self.caught_signal != NO_SIGNAL_CAUGHT:
                return

    def loop_forever(self):
        self.logger.log("startup", {"pid": os.getpid()})
        try:
            self.uncaught_loop_forever()
            if self.caught_signal == NO_SIGNAL_CAUGHT:
                raise RuntimeError("No error caught when exiting")
        except Exception as e:
            self.logger.log("exit", {"exception": repr(e)})
            raise (e)
        exit_reason = signal.strsignal(self.caught_signal)
        self.logger.log('exit', {"reason": exit_reason})

    def screenshot_now(self):
        return self.screenshot_handler.screenshot_now()

    def screenshots_expire_now(self):
        return self.screenshot_handler.screenshots_expire_now()

    def run_database_migrations(self):
        dsn = database.sqlite_dsn_from_dbfile(self.dbfile)
        database.run_migrations(dsn)


def handles(args):
    return (args.monitor_start_only or
            args.screenshot_now or
            args.show_detections or
            args.screenshots_expire_now)


def run_monitor(args):

    daemon = Daemon(args)

    if args.screenshot_now:
        files = daemon.screenshot_now()
        print(f"Created {', '.join(files)}")
        sys.exit(0)

    if args.show_detections:
        print("Executables:\n")
        print(external_dependencies.executables_status_string())
        print('-' * 60)
        detectors = activedetector.probe_detectors(args)
        print("Activity Detectors (the first working one will be used):\n")
        print(activedetector.detectors_status_string(detectors))

        screenshot_problems = screenshots.screenshot_problems()
        if screenshot_problems:
            print('-' * 60)
            print(f"Problems creating screenshots:\n\t{screenshot_problems}")
        sys.exit(0)

    if args.screenshots_expire_now:
        daemon.screenshots_expire_now()
        sys.exit(0)

    pidfilepath = os.path.expanduser(args.under_storage('daemon.pid'))
    with pidfile.PIDFile(pidfilepath):
        daemon.run_database_migrations()
        daemon.loop_forever()
