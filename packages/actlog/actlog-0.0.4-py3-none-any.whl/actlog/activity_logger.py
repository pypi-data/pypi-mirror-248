from __future__ import annotations

import os
import sys

import json
import time
import datetime
from dataclasses import dataclass
from collections.abc import Sequence
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from . import timestr
from . import database
from .dbmodel import Activity, ActivityLog


class Logger:
    def __init__(self, db_file):
        dsn = database.sqlite_dsn_from_dbfile(db_file)
        self.engine = create_engine(dsn)

    def log(self, activity, dict=None, t_log=None):
        if t_log == None:
            t_log = time.time()

        details = None
        if dict:
            details = json.dumps(dict)

        activity_log = ActivityLog(
            time=t_log,
            activity=Activity[activity],
            details=details
        )

        with Session(self.engine) as session:
            session.add(activity_log)
            session.commit()
            # print(activity_log)

        print("%s: %s %s" %
              (timestr.time_to_string(t_log), activity, details))
        sys.stdout.flush()


class Consumer:
    def __init__(self, db_file):
        dsn = database.sqlite_dsn_from_dbfile(db_file)
        self.engine = create_engine(dsn)

    def logs(self, t_from, t_to):
        if not t_to:
            # make it a little later than now to avoid race conditions
            t_to = time.time() + 60
        with Session(self.engine) as session:
            stmt = select(ActivityLog).\
                where(ActivityLog.time >= t_from).\
                where(ActivityLog.time < t_to)
            return session.scalars(stmt).all()

    def log_days(self, t_from, t_to, start_of_day):
        activityLogs = self.logs(t_from, t_to)
        day_periods = _DayPeriods(start_of_day)
        day_periods.store_rows(activityLogs)
        return day_periods.get_days()


@dataclass
class Period:
    start: float
    stop: float

    def duration(self):
        if not self.start:
            raise Exception('Periods need a start time')
        if self.stop:
            stop = self.stop
        else:
            stop = time.time()
        return stop - self.start


@dataclass
class Day:
    date: datetime.date
    periods: list[Period]


class _DayPeriods:
    """_DayPeriods turns a sequence of database rows into list[Day]

    The public interface is ActivityLogger().log_days()
    """

    def __init__(self, start_of_day):
        self.start_of_day = start_of_day
        self.current_date = None
        self.days = []
        self.curr_day_periods = []

    def get_date(self, t):
        return datetime.date.fromtimestamp(t - self.start_of_day * 3600)

    def end_current_day(self):
        if self.current_date == None:
            return
        old_day = Day(self.current_date, self.curr_day_periods)
        self.days.append(old_day)
        self.curr_day_periods = []
        self.current_date = None

    def add_period(self, start, stop):
        date = self.get_date(start)
        if self.current_date and self.current_date != date:
            self.end_current_day()
        self.current_date = date
        self.curr_day_periods.append(Period(start, stop))

    def store_rows(self, alogs: Sequence[ActivityLog]):
        start = None
        for alog in alogs:
            activity = alog.activity

            if activity.isActive():
                if start == None:
                    start = alog.time
                continue

            if start != None:
                self.add_period(start, alog.time)
                start = None
        if start != None:
            self.add_period(start, None)
        self.end_current_day()

    def get_days(self):
        return self.days
