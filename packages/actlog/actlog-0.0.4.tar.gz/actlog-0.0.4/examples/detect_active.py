import subprocess

from actlog import external_executables


def detection_problems(args):
    """Optional method that returns None or a string representing why this
    detector won't work."""
    if not external_executables.found('xprintidle'):
        return "xprintidle executable not found"
    return None


def is_active(args):
    """Returns True or False depending on whether the user is idle.

    This function will not be called if detection_problems() returns a
    problem"""
    result = subprocess.run(["xprintidle"], check=True, capture_output=True)
    stdout = result.stdout.rstrip().decode("utf-8")
    idle_seconds = int(stdout) / 1000
    return idle_seconds <= args.inactivity_time * 60
