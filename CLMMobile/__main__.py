from flask import Flask, redirect
from flask_socketio import SocketIO
from CLMMobile.base import Base 
from CLMMobile.timer import TimerBp
from CLMMobile.webclock import Webclock
from CLMMobile.admin import AdminBp
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import AuthBp, get_secret_key
from CLMMobile.utils.schedule_service.service import get_schedule_data_auto, convert
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR
from CLMMobile.utils.settings import Settings
from CLMMobile.utils.data import DataService
import socket

server = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
server.secret_key = get_secret_key()
socketio = SocketIO(server, async_mode="threading")
port = 5051

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(("10.20.30.40", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def setup():
    settings = Settings()
    trans = Translation(settings)
    db = DataService()
    
    # get the schedule for today
    schedule = get_schedule_data_auto()

    base = Base(server, trans, get_ip(), port)
    base.register()

    auth = AuthBp(server, trans)
    auth.register()

    admin = AdminBp(server, trans, auth.auth, db)
    admin.register()

    timer = TimerBp(server, socketio, trans, schedule, db)
    timer.register()

    webclock = Webclock(server, socketio, timer=timer.clock)
    webclock.register()


if __name__ == "__main__":
    setup()
    socketio.run(app=server, host="0.0.0.0", port=port, debug=True, allow_unsafe_werkzeug=True)