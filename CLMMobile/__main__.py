from flask import Flask, redirect
from flask_socketio import SocketIO
from CLMMobile.base import Base 
from CLMMobile.timer import TimerBp
from CLMMobile.webclock import Webclock
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import AuthBp, get_secret_key
from CLMMobile.utils.schedule_service.service import get_schedule_data_auto, convert
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR
from CLMMobile.utils.settings import Settings
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
    
    # get the schedule for today
    schedule = convert(get_schedule_data_auto(), trans)

    base = Base(server, get_ip(), port)
    base.register()

    auth = AuthBp(server)
    auth.register()

    timer = TimerBp(server, socketio, trans, schedule)
    timer.register()

    webclock = Webclock(server, socketio, timer=timer.clock)
    webclock.register()


if __name__ == "__main__":
    setup()
    socketio.run(app=server, host="0.0.0.0", port=port, debug=True, allow_unsafe_werkzeug=True)