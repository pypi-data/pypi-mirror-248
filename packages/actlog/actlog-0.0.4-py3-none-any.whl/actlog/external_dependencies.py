from __future__ import annotations

import sys
import os
from textwrap import dedent

import subprocess

from .activedetector.dbusscreensaver import dbusScreensaverDetectorClasses


def find(execubale):
    try:
        result = subprocess.run(("command -v %s" % (execubale,)),
                                shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return False
    return result.stdout.decode().rstrip()


def executables_status_string():
    executablesData = [
        ['scrot', 'Best at taking screenshots'],
        ['import', 'OK at taking screenshots'],
        ['convert', 'Reduces screenshots size'],
        ['pngquant', 'Compresses screenshots'],
        ['dbus-send', 'Used to detect screensavers'],
        ['xprintidle',
         'Fallback activity detector if screensaver could not be detected'],
    ]

    max_len = 0
    for executableData in executablesData:
        executable, reason = executableData
        if len(executable) > max_len:
            max_len = len(executable)

    strings = []
    for executableData in executablesData:
        executable, reason = executableData
        was_found = find(executable)
        string = f"{executable}:\n"
        if was_found:
            string += f"\tWas found as {was_found}\n"
        else:
            string += "\t*Was not found*\n"
        string += f"\t{reason}\n"
        strings.append(string)
    return "\n".join(strings)


def check_dependencies(args):
    packages = set()
    messages = []
    required_missing = False

    # Screenshots
    if not find('scrot') and not find('import'):
        messages.append(
            """
            To create screenshots, please make scrot or import available.

            In Debian and Ubuntu they are in the scrot and imagemgick packages
            respectively.
            """)
        packages.add('scrot')
        packages.add('imagemagick')
        required_missing = True
    if not find('convert'):
        messages.append(
            """
            To reduce screenshot color depth in order to reduce file size,
            optionally make convert available.

            In Debian and Ubuntu it is in the imagemgick package.
            """)
        packages.add('imagemagick')
    if not find('pngquant'):
        messages.append(
            """
            To compress screenshots, optionally make pngquant available.

            In Debian and Ubuntu it is in the pngquant package.
            """)
        packages.add('pngquant')

    need_xprintidle = True
    for Cls in dbusScreensaverDetectorClasses:
        instance = Cls(args)
        if not instance.detection_problems():
            need_xprintidle = False
            break
    if need_xprintidle:
        if not find('xprintidle'):
            messages.append(
                """
                To detect user active/idle, make xprintidle available.

                In Debian and Ubuntu it is in the xprintidle package.
                """)
            packages.add('xprintidle')
            required_missing = True

    if len(messages):
        for m in messages:
            mess = dedent(m).strip()
            print(mess)
            print("-" * 20)
        if len(packages):
            print()
            print("In Debian or Ubuntu, please install the packages with:")
            print("sudo apt install " + " ".join(sorted(packages)))
        if required_missing:
            print()
            print('Exiting because required executables are missing.')
            sys.exit(1)
        # else
        print("#" * 40)
    elif required_missing:
        raise RuntimeError('How could required packages be missing '
                           'without there being any messages?')
