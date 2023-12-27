import os.path
import subprocess

from . import helpformatter
from . import screenshots
from .timestr import parse_string_to_time

def add_parser(subparsers):
    help = "View screenshots for a time period."

    parser = subparsers.add_parser('view',
        formatter_class=helpformatter.All,
        help=help,
        description=help)

    parser.add_argument(
        '--from',
        type=str,
        default="yesterday 00:00",
        metavar="TIME",
        help="Show logs from this time")

    parser.add_argument(
        '--to',
        type=str,
        default=None,
        metavar="TIME",
        help="Show logs until this time")

    parser.add_argument(
        '--viewer',
        type=str,
        default=None,
        metavar="TIME",
        help="Image viewer that takes filenames as parameters, e.g. eog")

    parser.add_argument(
        '--show-all',
        action='store_const',
        const=True,
        help="Also show screenshots with metadata.")

    parser.set_defaults(func=subcommand, config_key='view')

def subcommand(args):
    # 'from' is a reserved word
    t_from = parse_string_to_time(vars(args)['from'])
    if args.to:
        t_to = parse_string_to_time(args.to)
    else:
        t_to = None
    # print(f"from: {t_from} to: {t_to}")
    screenshots_dir = args.under_storage('screenshots')
    screenshot_consumer = screenshots.Consumer(screenshots_dir)
    shots = screenshot_consumer.list_screenshots(t_from, t_to)
    screenshot_key = 'unsafe' if args.show_all else 'safe'
    def file_from_shot(s):
        return os.path.join(screenshots_dir, s[screenshot_key]) + '.png'
    files = list(map(file_from_shot, shots))
    if args.viewer:
        subprocess.run([args.viewer, *files])
    else:
        print(" ".join(files))