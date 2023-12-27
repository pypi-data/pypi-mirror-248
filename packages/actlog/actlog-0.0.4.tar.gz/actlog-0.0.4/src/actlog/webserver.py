import os
import sys
import datetime
import typing
import argparse
import secrets
import functools

import flask
from flask import Flask, jsonify, send_from_directory, request, session
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from furl import furl

from . import activity_logger
from . import screenshots
from . import database
from .dbmodel import Configuration
from .webpassword import verify_password


# Could easily be made into an argparse argument
GUNICORN_WORKERS = 3


def add_parser_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--port',
        type=int,
        default=1250,
        metavar="PORT",
        help="The port to run the webserver on")

    parser.add_argument(
        '--ip-address',
        type=str,
        default='localhost',
        metavar="IP",
        help="The IP address to bind the webserver to")


class DateJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj: typing.Any) -> typing.Any:  # type: ignore
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return DefaultJSONProvider.default(obj)


def time_args_from_request():
    def int_arg(key: str) -> int | None:
        str_arg = request.args.get(key)
        if str_arg == None:
            return None
        return int(str_arg)

    t_from = int_arg('from')
    if t_from == None:
        raise RuntimeError('Need a from parameter')
    t_to = int_arg('to')
    start_of_day = int_arg('startOfDay')
    if start_of_day == None:
        raise RuntimeError('Need a start_of_day parameter')
    return dict(t_from=t_from, t_to=t_to, start_of_day=start_of_day)

# in order to run nicely under gunicorn, we prefer configuation with environment
# variables here. The envs used are:
# DEVELOPMENT_CORS: If it exists and is truthy, disable CORS
# STORAGE: The directory under which to find screenshots and database file


def create_app():

    app = Flask(__name__)
    app.json = DateJSONProvider(app)

    # use env if exists (for development - see <projroot>/actdevel.sh),
    # otherwise default to ./frontend/build (in installed package)
    frontend_build = os.environ.get('FRONTEND_BUILD') or \
        os.path.join(os.path.dirname(__file__), 'frontend', 'build')
    # print('frontend_build', frontend_build)

    # CORS should perhaps not depend on --debug
    if os.environ.get('DEVELOPMENT_CORS'):
        CORS(app, supports_credentials=True)

    storage = os.environ.get('STORAGE')
    if not storage or not os.path.isdir(storage):
        raise RuntimeError('Need STORAGE environ to point to '
                           'an actlog storage dir')
    db_file = os.path.join(storage, 'actlog.db')

    dsn = database.sqlite_dsn_from_dbfile(db_file)
    engine = create_engine(dsn)

    def get_session_key():
        with Session(engine) as session:
            stmt = select(Configuration)
            configuration = session.scalars(stmt).first()
            if configuration.session_key is None:
                configuration.session_key = secrets.token_hex(32)
                session.commit()
            return configuration.session_key

    app.config['SECRET_KEY'] = bytes.fromhex(get_session_key())
    app.config['SESSION_COOKIE_NAME'] = 'actlog-session'

    screenshots_dir = os.path.join(storage, 'screenshots')
    screenshot_consumer = screenshots.Consumer(screenshots_dir)

    def login_required(wants_json):
        def login_required_wrapper(func):
            @functools.wraps(func)
            def new_function(*args, **kwargs):
                if not 'loggedin' in session:
                    if (wants_json):
                        response = jsonify({'message':'Not logged in'})
                        return response, 401
                    else:
                        return flask.redirect(flask.url_for('login'))
                return func(*args, **kwargs)
            return new_function
        return login_required_wrapper

    @app.route('/')
    @login_required(wants_json=False)
    def root():
        # print('serving / from', frontend_build)
        return send_from_directory(frontend_build, 'index.html')

    @app.route('/login', methods=['POST'])
    def login():
        password = request.form.get('password')
        if not verify_password(storage, password):
            url = furl(flask.url_for('login'))
            url.args['message'] = 'Invalid Password'
            return flask.redirect(url.url)
        session['loggedin'] = 1
        if (os.environ.get('FOLLOW_ANY_NEXT_REDIRECTS') and
            request.form.get('next_url')):
            next_url = request.form.get('next_url')
        else:
            next_url = flask.url_for('root')
        return flask.redirect(next_url)

    @app.route('/logout', methods=['GET'])
    def logout():
        del session['loggedin']
        return jsonify(None)

    @app.route('/<path:path>')
    def send_build(path: str):
        # This avoids us having to set
        # export const trailingSlash = 'always'
        # in frontend/src/routes/+layout.js
        # See note about trailingSlash in
        # https://kit.svelte.dev/docs/adapter-static
        fullpath = os.path.join(frontend_build, path)
        if not os.path.exists(fullpath) and os.path.exists(fullpath + ".html"):
            path += ".html"

        # print('serving: %s' % os.path.join(frontend_build, path))
        return send_from_directory(frontend_build, path)

    @app.route('/screenshots')
    @login_required(wants_json=True)
    def shots():
        time_args = time_args_from_request()
        return jsonify(screenshot_consumer.screenshot_days(
            **time_args
        ))

    @app.route('/screenshot/<path:path>')
    @login_required(wants_json=True)
    def screenshot(path: str):
        return send_from_directory(
            screenshot_consumer.screenshots_dir, path + '.png'
        )

    @app.route('/log')
    @login_required(wants_json=True)
    def log():
        time_args = time_args_from_request()
        log_consumer = activity_logger.Consumer(db_file)

        logs = log_consumer.log_days(**time_args)
        return jsonify(logs)

    return app


def run_webserver(args, dev_mode=False):
    print('Running webserver, dev_mode:', dev_mode)

    os.environ['STORAGE'] = os.path.expanduser(args.storage)
    if dev_mode:
        os.environ['DEVELOPMENT_CORS'] = "1"
        # This can be dangerous - only in dev mode
        os.environ['FOLLOW_ANY_NEXT_REDIRECTS'] = "1"
        app = create_app()
        app.run(host=args.ip_address, port=args.port, debug=True)
    else:
        # Assume gunicorn executable is in the same directory as the current
        # python executable.
        gunicorn = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
        command = [
            gunicorn,
            '-w', str(GUNICORN_WORKERS),
            '--bind', f"{args.ip_address}:{args.port}",
            '--capture-output',
            'actlog.webserver:create_app()'
        ]
        os.execvp(command[0], command)
