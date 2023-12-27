import os
import subprocess
from ..external_dependencies import find
class Xprintidle:
    def __init__(self, args):
        self.args = args

    def name(self):
        return  'Standard active detector'


    def is_active(self):
        """Returns True or False depending on whether the user is idle.

        This function will not be called if detection_problems() returns a
        problem"""
        result = subprocess.run(["xprintidle"], check=True, capture_output=True)
        stdout = result.stdout.rstrip().decode("utf-8")
        idle_seconds = int(stdout) / 1000
        return idle_seconds <= self.args.inactivity_time * 60

    def detection_problems(self):
        if not os.environ.get('DISPLAY'):
            return "No DISPLAY environment variable set"
        if os.environ.get('WAYLAND_DISPLAY'):
            return "xprintidle doesn't work under wayland"
        if not find('xprintidle'):
            return "Could not find the xprintidle executable"
        return None