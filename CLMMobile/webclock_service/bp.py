from flask import Flask, Blueprint, render_template, jsonify
from flask_socketio import SocketIO
import pathlib

class WebclockService:
    FILE = pathlib.Path(__file__).resolve().parent
    NAMESPACE = "/webclockservice"

    def __init__(self, app: Flask, socketio: SocketIO):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("webclock_service", __name__,
                            template_folder=str(self.FILE / "./templates"),
                            static_folder=str(self.FILE.parent / "./assets"),
                            url_prefix=self.NAMESPACE)
        self.socketio: SocketIO = socketio

        self.register_endpoints()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/", "webclock", self.webclock_endpoint, methods=["GET"])

    # endpoints
    def webclock_endpoint(self):
        return render_template("webclock.html")