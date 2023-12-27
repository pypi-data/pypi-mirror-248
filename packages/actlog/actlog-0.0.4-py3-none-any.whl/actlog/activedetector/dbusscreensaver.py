"""GNOME screensaver detector

It detects user activity by seeing if the screensaver is active.

See also
https://unix.stackexchange.com/questions/197032/detect-if-screensaver-is-active

## Periodic error

I have seen this error periodically but don't (yet) know why:

```
RuntimeError: dbus-send returned a non-zero status: 1
stderr: Error org.freedesktop.DBus.Error.NoReply: Did not receive a reply.
Possible causes include: the remote application did not send a reply,
the message bus security policy blocked the reply, the reply timeout expired,
or the network connection was broken.
```

(it was all in one line)

"""
import subprocess
import os


class NotImplemented(Exception):
    def __str__(self):
        return "Not implemented in DBUS"


def run_generic_dbus(dest, object_path, interface_member):
    """run_dbus tries to detect gnome screensaver with dbus-send

    If it encounters any problems or unexpected output, it will throw an
    Exception
    """
    completed = subprocess.run([
        'dbus-send',
        '--print-reply=literal',
        f'--dest={dest}',
        object_path,
        interface_member,
    ], shell=False, check=False, capture_output=True)
    if completed.returncode != 0:
        stdout_str = completed.stdout.decode().rstrip()
        stderr_str = completed.stderr.decode().rstrip()
        if stderr_str.startswith(
            "Error org.freedesktop.DBus.Error.NotSupported"
        ):
            raise NotImplemented()
        error_messages = [
            'dbus-send returned a non-zero status: ' +
            completed.returncode.__str__()
        ]
        if stdout_str != '':
            error_messages.append(f"stdout: {stdout_str}")
        if stderr_str != '':
            error_messages.append(f"stderr: {stderr_str}")
        raise RuntimeError(" ".join(error_messages))
    if completed.stdout == b'   boolean false\n':
        return True
    if completed.stdout == b'   boolean true\n':
        return False
    raise RuntimeError(
        'Unexpected output from dbus-send' + completed.stdout.decode()
    )


class DbusScreensaverDetector:
    def __init__(
        self,
        name_prefix,
        dest,
        object_path,
        interface_member,
        args,
    ):
        self.name_prefix = name_prefix
        self.dest = dest
        self.object_path = object_path
        self.interface_member = interface_member
        self.args = args

    def name(self):
        return f'{self.name_prefix} screensaver detector'

    def run_dbus(self):
        return run_generic_dbus(
            self.dest,
            self.object_path,
            self.interface_member
        )

    def is_active(self):
        return self.run_dbus()

    def detection_problems(self):
        if self.args.no_screensaver_detection:
            return "Disabled by --no-screensaver-detection"
        try:
            self.run_dbus()
        except Exception as e:
            return e.__str__()
        return None


class GnomeScreensaverDetector(DbusScreensaverDetector):
    def __init__(self, args):
        super().__init__(
            'GNOME',
            'org.gnome.ScreenSaver',
            '/org/gnome/ScreenSaver',
            'org.gnome.ScreenSaver.GetActive',
            args
        )


class FreedesktopScreensaverDetector(DbusScreensaverDetector):
    def __init__(self, args):
        super().__init__(
            'Generic Freedesktop /ScreenSaver',
            'org.freedesktop.ScreenSaver',
            '/ScreenSaver',
            'org.freedesktop.ScreenSaver.GetActive',
            args
        )


class FreedesktopFullPathScreensaverDetector(DbusScreensaverDetector):
    def __init__(self, args):
        super().__init__(
            'Generic Freedesktop /org/freedesktop/ScreenSaver',
            'org.freedesktop.ScreenSaver',
            '/org/freedesktop/ScreenSaver',
            'org.freedesktop.ScreenSaver.GetActive',
            args
        )


dbusScreensaverDetectorClasses = [
    GnomeScreensaverDetector,
    FreedesktopScreensaverDetector,
    FreedesktopFullPathScreensaverDetector
]
