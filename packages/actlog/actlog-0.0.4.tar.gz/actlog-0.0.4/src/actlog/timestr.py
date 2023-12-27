# pyright: strict

import datetime
import time
import dateparser

def time_to_string(t: float) -> str:
    time_format = "%F %T.{millis} %Z"
    # use the first 3 digits after the '.' when converted to string
    millis = repr(t).split('.')[1][:3]
    return time.strftime(time_format, time.localtime(t)).format(millis=millis)

def parse_string_to_time(str: str) -> float:
    dt = dateparser.parse(str)
    if dt == None:
        raise Exception(
            "Couldn't parse \"%s\" with dateparser.parse()" % str
        )
    return datetime.datetime.timestamp(dt)
