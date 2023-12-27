import os
import getpass

import argon2
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from . import database

from .dbmodel import Configuration

_PAM_HASH = "__USE_PAM__"


def create_engine_under_storage(storage):
    if not storage or not os.path.isdir(storage):
        raise RuntimeError('Need storage to point to an actlog storage dir')
    db_file = os.path.join(storage, 'actlog.db')
    dsn = database.sqlite_dsn_from_dbfile(db_file)
    return create_engine(dsn)


def _set_password_hash(storage, hash):
    engine = create_engine_under_storage(storage)
    with Session(engine) as session:
        stmt = select(Configuration)
        configuration = session.scalars(stmt).first()
        configuration.password_hash = hash
        session.commit()


def set_password_pam(storage):
    try:
        import pam
    except ImportError as e:
        raise RuntimeError("PAM not supported - couldn't import 'pam' module:")
    _set_password_hash(storage, _PAM_HASH)


def set_password_argon2(storage, password):
    ph = argon2.PasswordHasher()
    hash = ph.hash(password)
    _set_password_hash(storage, hash)


def _verify_password_pam(password):
    import pam
    return pam.authenticate(getpass.getuser(), password)


def _verify_password_argon2(storage, hash, password):
    ph = argon2.PasswordHasher()
    try:
        good = ph.verify(hash, password)
        if ph.check_needs_rehash(hash):
            set_password_argon2(storage, password)
    except argon2.exceptions.VerifyMismatchError:
        good = False
    return good


def verify_password(storage, password):
    engine = create_engine_under_storage(storage)
    with Session(engine) as session:
        stmt = select(Configuration)
        configuration = session.scalars(stmt).first()
        if configuration.password_hash == _PAM_HASH:
            return _verify_password_pam(password)
        else:
            return _verify_password_argon2(
                storage, configuration.password_hash, password)
