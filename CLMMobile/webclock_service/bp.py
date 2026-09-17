from flask import Flask, Blueprint, render_template, jsonify
from flask_socketio import SocketIO
import pathlib


class WebclockService:
    FILE = pathlib.Path(__file__).resolve().parent.parent
    NAMESPACE = "/webclockservice"

    def __init__(self, app: Flask, socketio: SocketIO, timer, trans):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("webclock_service", __name__,
                            template_folder=str(self.FILE / "assets/templates"),
                            static_folder=str(self.FILE / "assets/static"),
                            url_prefix=self.NAMESPACE)
        self.socketio: SocketIO = socketio
        self.timer = timer
        self.trans = trans  # translation service

        self.register_endpoints()
        self.register_sockets()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/", "webclock", self.webclock_endpoint, methods=["GET"])

    def register_sockets(self):
         self.socketio.on_event("connect", self.connect, namespace=self.NAMESPACE)

    # endpoints
    def webclock_endpoint(self):
        return render_template("webclock_service/index.html")

    def connect(self):
        self.socketio.emit("status", {
            "timer_started": self.timer.running,
            "current": self.timer.schedule[self.timer.current].to_dict(self.trans)
        },
        namespace=self.NAMESPACE)