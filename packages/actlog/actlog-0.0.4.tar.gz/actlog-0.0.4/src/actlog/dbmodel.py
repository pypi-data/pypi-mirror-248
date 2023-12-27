# pyright: strict

"""Database and migrations

Short version:

The database contains a alembic_version.version_num that is the current version.

See:

* https://docs.sqlalchemy.org/en/20/orm/quickstart.html
* https://alembic.sqlalchemy.org/en/latest/tutorial.html

To create a schema update:

* Make a change to one of the classes derived from Base below
* Run DBFILE=$HOME/.actlog/storage/actlog.db ./dev alembic -c src/actlog/migrations/alembic.ini revision --autogenerate -m ${MSG?Need a msg}
* Check the created file for correctness
* Run
    * cp ~/.actlog/storage/actlog.db /tmp
    * DBFILE=$HOME/.actlog/storage/actlog.db ./dev alembic -c src/actlog/migrations/alembic.ini upgrade head

If that works you can rm /tmp/actlog.db
"""

import enum

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import String, Float, Enum

from . import timestr


class Base(DeclarativeBase):
    pass


class Activity(enum.Enum):
    startup = 1
    active = 2
    inactive = 3
    exit = 4

    def isActive(self):
        activityIsActive = {
            Activity.startup: True,
            Activity.active: True,
            Activity.inactive: False,
            Activity.exit: False,
        }
        if not self in activityIsActive:
            raise RuntimeError(f'Unknown Activity: {self}')
        return activityIsActive[self]


class ActivityLog(Base):
    __tablename__ = "activity_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[float] = mapped_column(Float(), nullable=False)
    activity: Mapped[Activity] = mapped_column(
        Enum(Activity), nullable=False)
    details: Mapped[str] = mapped_column(String(512), nullable=True)

    def __repr__(self) -> str:
        return f"ActivityLog(id={self.id}, " \
               f"time: {self.time} ({timestr.time_to_string(self.time)}) " \
               f"activity: {repr(self.activity)} details: {self.details})"

class Configuration(Base):
    __tablename__ = "configuration"
    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(250), nullable=True)
    session_key: Mapped[str] = mapped_column(String(32), nullable=True)

    def __repr__(self) -> str:
        return f"Configuration(id={self.id}, " \
               f"password_hash: {self.password_hash} " \
               f"session_key: {repr(self.session_key)})"
