import time
import datetime

import dateparser

from . import helpformatter
from . import activity_logger
from .timestr import parse_string_to_time

start_of_day_long = """\
How many hours after midnight to still count as the previous day

E.g. a value of 2 will mean that for e.g. a Saturday, any start times
from Saturday 02:00AM until Sunday 02:00AM will be counted as Saturday.

Good for night owls that often work after midnight but want such periods
to be counted for the previous day.
"""

def add_parser(subparsers):
    help = "Show a log of your activity."

    parser = subparsers.add_parser('log',
        formatter_class=helpformatter.All,
        help=help,
        description=help)

    parser.add_argument(
        '--from',
        type=str,
        default="00:00 a week ago",
        metavar="TIME",
        help="Show logs from this time")

    parser.add_argument(
        '--to',
        type=str,
        default=None,
        metavar="TIME",
        help="Show logs until this time")

    parser.add_argument(
        '--start-of-day',
        type=int,
        default=0,
        metavar="HOURS",
        help=start_of_day_long)

    parser.set_defaults(func=subcommand, config_key='log')

def format_time(format, t):
    return time.strftime(format, time.localtime(t))

def duration_string(duration):
    # Round to "nearest" minute
    duration += 30
    hours = int(duration / 3600)
    min = int(duration / 60) % 60
    return "%02d:%02d" % (hours, min)

def subcommand(args):
    # 'from' is a reserved word
    t_from = parse_string_to_time(vars(args)['from'])
    if args.to:
        t_to = parse_string_to_time(args.to)
    else:
        t_to = None
    # print(f"from: {t_from} to: {t_to} startOfDay: {args.start_of_day}")

    log_consumer = activity_logger.Consumer(args.under_storage('actlog.db'))

    days = log_consumer.log_days(t_from, t_to, args.start_of_day)

    first_day = True
    for day in days:
        if not first_day:
            print()
        first_day = False
        duration = 0
        for p in day.periods:
            duration += p.duration()
        print('### %s: Total: %s' %
              ( day.date.strftime("%a %F"), duration_string(duration) ))
        print()
        for p in day.periods:
            duration = p.duration()
            # Don't show durations less than a minute - they're mostly noise
            if duration < 60:
                continue
            if p.stop:
                stop_str = format_time("%H:%M", p.stop)
            else:
                stop_str = '  ?  '
            print('  %s -> %s : %s' % (
                format_time("%H:%M", p.start),
                  stop_str,
                  duration_string(duration)))
