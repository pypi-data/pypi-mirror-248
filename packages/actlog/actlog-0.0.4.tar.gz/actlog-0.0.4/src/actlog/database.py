"""See doc in dbmodel.py"""

import os
import sys
from alembic.config import Config
from alembic import command

def sqlite_dsn_from_dbfile(dbfile: str) -> str:
    return f'sqlite:///{dbfile}'

def run_migrations(dsn: str) -> None:
    script_location = os.path.join(os.path.dirname(__file__), 'migrations')
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Need script_location and dbfile')
        sys.exit(1)
    dsn = sqlite_dsn_from_dbfile(sys.argv[1])
    run_migrations(dsn)