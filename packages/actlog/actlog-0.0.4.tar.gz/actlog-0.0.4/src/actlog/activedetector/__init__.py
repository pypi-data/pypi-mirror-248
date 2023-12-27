import traceback
from . import custom
from . import xprintidle
from .custom import CustomActiveDetector
from .executablerunning import ExecutableRunning
from .dbusscreensaver import dbusScreensaverDetectorClasses
from .xprintidle import Xprintidle

def getActiveDetectorClasses():
    activeDetectorClasses = []

    activeDetectorClasses.append(CustomActiveDetector)
    activeDetectorClasses.append(ExecutableRunning)

    for cls in dbusScreensaverDetectorClasses:
        activeDetectorClasses.append(cls)

    activeDetectorClasses.append(Xprintidle)
    return activeDetectorClasses


def probe_detectors(args):
    detectors = []
    for Cls in getActiveDetectorClasses():
        instance = Cls(args)
        problems = None
        if hasattr(instance, 'detection_problems'):
            problems = instance.detection_problems()
        is_active = None
        if problems is None:
            try:
                is_active = instance.is_active()
            except Exception:
                print(traceback.format_exc())
        detectors.append((instance, problems, is_active))
    return detectors


def detectors_status_string(detectors):
    substrings = []
    best_detector = find_detector(detectors)
    for detector in detectors:
        instance, problems, is_idle = detector
        string = ""
        # print(best_detector, detector)
        if instance == best_detector:
            string += "**Using this one**: "
        string += f"{instance.name()}:\n\t"
        if problems is None:
            string += f"Working - is active: {is_idle}"
        else:
            string += f"Not working because: {problems}"
        substrings.append(string)

    # substrings.append("Using best working detector:\n\t"
    #                   f"{best_detector.name()}")

    return "\n\n".join(substrings)


def find_detector(detectors):
    for detector in detectors:
        instance, problems, _ = detector
        if problems is None:
            return instance
    return None