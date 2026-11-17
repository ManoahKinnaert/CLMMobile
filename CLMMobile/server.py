import logging

from flask import Flask, cli as flask_cli
from flask_socketio import SocketIO

from CLMMobile.base import Base
from CLMMobile.timer import TimerBp
from CLMMobile.webclock import Webclock
from CLMMobile.admin import AdminBp
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import AuthBp, get_secret_key
from CLMMobile.utils.settings import Settings
from CLMMobile.utils.data import DataService
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR
from CLMMobile.utils.console import *
from CLMMobile.utils.schedule_service.service import get_schedule_data_auto

server = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

server.secret_key = get_secret_key()

socketio = SocketIO(
    server,
    async_mode="threading",
    cors_allowed_origins="*"
)

port = 5051


def _silence_dev_server():
    flask_cli.show_server_banner = lambda *args, **kwargs: None
    logging.getLogger("werkzeug").setLevel(logging.ERROR)


def setup():
    settings = Settings()
    trans = Translation(settings)
    db = DataService()

    schedule = get_schedule_data_auto()

    BASE = Base(server, trans, port)
    BASE.register()

    auth = AuthBp(server, trans)
    auth.register()

    admin = AdminBp(server, trans, auth.auth, db)
    admin.register()

    timer = TimerBp(server, socketio, trans, schedule, db)
    timer.register()

    webclock = Webclock(server, socketio, timer=timer.clock)
    webclock.register()

    return BASE, trans

def run():
    _silence_dev_server()
    setup()

    socketio.run(
        app=server,
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
        log_output=False
    )

def run_tui(trans, BASE):
    print(chr(27) + "[2J")

    strings = trans.get_string_section("console")

    startup_view(
        strings=strings,
        global_ip=BASE.get_ip(),
        port=port
    )

    while True:
        try:
            if user_input(f"{strings['close']}: ").lower() == "q":
                break

        except KeyboardInterrupt:
            break
