from flask import Flask, Blueprint, render_template, jsonify
from flask_socketio import SocketIO
import pathlib 

from .timer import Timer


class TimeService:
    FILE = pathlib.Path(__file__).resolve().parent
    NAMESPACE = "/timeservice"

    def __init__(self, app: Flask, socketio: SocketIO):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("time_service", __name__,
                            template_folder=str(self.FILE / "./templates"), 
                            static_folder=str(self.FILE.parent / "./assets"),
                            url_prefix=self.NAMESPACE)

        self.socketio: SocketIO = socketio
        self.timer = Timer(socketio=self.socketio)

        self.register_endpoints()
        self.register_sockets()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/control", "control", self.control_endpoint, methods=["GET"])
        self.bp.add_url_rule("/schedule", "schedule", self.get_schedule, methods=["GET"])
        self.bp.add_url_rule("/schedule/current", "current", self.get_current, methods=["GET"])

    def register_sockets(self):
        # timer control
        self.socketio.on_event("connect", self.emit_status, namespace=self.NAMESPACE)
        self.socketio.on_event("toggle", self.toggle, namespace=self.NAMESPACE)

    def toggle(self):
        if self.timer.running: self.timer.stop()
        else: self.timer.start()
        # emit status
        self.emit_status()
        
    def emit_status(self):
        print("status")
        self.socketio.emit("status", {
            "timer_started": self.timer.running,
            "current": self.timer.schedule[self.timer.current].to_dict()
            }, 
            namespace=self.NAMESPACE)

    # endpoints and websocket stuff
    def control_endpoint(self):
        return render_template("index.html")

    def get_schedule(self):
        schedule = self.timer.schedule
        return jsonify([talk.to_dict() for talk in schedule])

    def get_current(self):
        return jsonify(self.timer.schedule[self.timer.current].to_dict())