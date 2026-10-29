from flask import Blueprint, Flask, render_template
from flask_socketio import SocketIO
import CLMMobile.utils as utils

class TimerBp:
    NAMESPACE = "/timer"
    def __init__(self, server: Flask, socketio: SocketIO):
        """
        Timer blueprint template class.
        """
        self._server: Flask = server 
        self._bp: Blueprint = Blueprint("timer", 
                                        __name__,
                                        template_folder=utils.TEMPLATES_DIR / "timer",
                                        static_folder=utils.STATIC_DIR,
                                        url_prefix=self.NAMESPACE)
        self._socketio: SocketIO = socketio
        
    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "control", self.index, methods=["GET"])

    def register_sockets(self):
        self._socketio.on_event("connect", self.connect, namespace=self.NAMESPACE)
        self._socketio.on_event("toggle", self.toggle, namespace=self.NAMESPACE)
        self._socketio.on_event("next", self.next, namespace=self.NAMESPACE)
        self._socketio.on_event("prev", self.prev, namespace=self.NAMESPACE)
        self._socketio.on_event("set_current", self.set_current, namespace=self.NAMESPACE)

    def connect(self):
        self._socketio.emit("connect_event", {
            "timer_started": True,
            "schedule": [],
            "current": 0
        }, namespace=self.NAMESPACE)

    def emit_status(self):
        self._socketio.emit("status", {
            "timer_started": True,
            "current": []
        })

    def toggle(self):
        pass 

    def next(self):
        pass 

    def prev(self):
        pass 

    def set_current(self):
        pass

    def login(self):
        pass 

    def index(self):
        return render_template("timer/index.html")