import time
import datetime

time_format = '%Y-%m-%d_%H:%M:%S%z'

def time_to_string(t):
    return time.strftime(time_format, time.localtime(t))

def string_to_time(string):
    dt = datetime.datetime.strptime(string, time_format)
    return time.mktime(dt.timetuple())

