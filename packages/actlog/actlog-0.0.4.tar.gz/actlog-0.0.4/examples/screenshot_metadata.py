import subprocess

# This is an example of a custom screenshot metedata generator. It uses the
# wmctrl utiltity (must be explicity installed) to see if there are any current
# windows with the title "VeryPrivate", and if os, the private: true is added to
# the screenshot metedata.

def metadata():
    result = subprocess.run("wmctrl -l | grep -q '\sVeryPrivate$'", shell=True);
    if result.returncode == 0:
        return {
            "private": True
        }
    else:
        return {}
