from flask import Blueprint, Flask, render_template
from flask_socketio import SocketIO
import CLMMobile.utils as utils

class TimerBp:
    def __init__(self, server: Flask, socketio: SocketIO):
        """
        Timer blueprint template class.
        """
        self._server: Flask = server 
        self._bp: Blueprint = Blueprint("timer", 
                                        __name__,
                                        template_folder=utils.TEMPLATES_DIR / "timer",
                                        static_folder=utils.STATIC_DIR,
                                        url_prefix="/timer")
        self._socketio: SocketIO = socketio
        
    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "timer", self.index, methods=["GET"])

    def register_sockets(self):
        pass 

    def connect(self):
        self._socketio.emit("connect_event", {
            "timer_started": True,
            "schedule": [],
            "current": 0
        }, namespace="/timer")

    def emit_status(self):
        self._socketio.emit("status", {
            "timer_started": True,
            "current": []
        })

    def login(self):
        pass 

    def index(self):
        return render_template("index.html")