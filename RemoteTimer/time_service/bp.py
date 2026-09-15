from flask import Flask, Blueprint, render_template
from flask_socketio import SocketIO
import pathlib 


class TimeService:
    FILE = pathlib.Path(__file__).resolve().parent

    def __init__(self, app: Flask, socketio: SocketIO):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("time_service", __name__,
                            template_folder=str(self.FILE / "./templates"), 
                            static_folder=str(self.FILE.parent / "./assets"),
                            url_prefix="/timeservice")

        self.socketio: SocketIO = socketio

        self.register_endpoints()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/control", "control", self.control_endpoint, methods=["GET"])

    # endpoints and websocket stuff
    def control_endpoint(self):
        return render_template("index.html")