from flask import Flask, Blueprint, render_template, jsonify 
from flask_socketio import SocketIO
from CLMMobile.timer import Timer
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR

class Webclock:

    NAMESPACE = "/webclock"

    def __init__(self, server: Flask, socketio: SocketIO, timer: Timer):
        self._server: Flask = server 
        self._bp: Blueprint = Blueprint("webclock", __name__,
                                       template_folder=TEMPLATES_DIR / "webclock",
                                       static_folder=STATIC_DIR,
                                       url_prefix=self.NAMESPACE)
        self._socketio: SocketIO = socketio
        self._timer: Timer = timer

    def register(self):
        self.register_sockets()
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "webclock", self.webclock_endpoint, methods=["GET"])

    def register_sockets(self):
        self._socketio.on_event("connect", self.connect, namespace=self.NAMESPACE)

    def webclock_endpoint(self):
        return render_template("webclock/index.html")

    def connect(self):
        self._socketio.emit("status", {
            "timer_started": self._timer.running,
            "current": self._timer.schedule[self._timer.current]
        },
        namespace=self.NAMESPACE)