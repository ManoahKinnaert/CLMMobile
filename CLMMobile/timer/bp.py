from flask import Blueprint, Flask, render_template
from flask_socketio import SocketIO
import CLMMobile.utils as utils
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import role_required, socket_role_required
from CLMMobile.utils.data import DataService
from CLMMobile.utils.schedule_service.service import get_schedule_data_auto, convert, ciruit_overseer_schedule
from .timer import Timer

class TimerBp:
    NAMESPACE = "/timer"
    def __init__(self, server: Flask, socketio: SocketIO, trans: Translation, db: DataService):
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
        self._trans: Translation = trans
        self._db: DataService = db
        self._timer: Timer = Timer(socketio, db)
        
        self.normal_mode()
        #self.circuit_overseer_mode()

    @property
    def clock(self): return self._timer

    def circuit_overseer_mode(self):
        if not self._timer.running:
            ciruit_overseer_schedule(self._timer.schedule, self._trans)
            if self._timer.current + 1 > len(self._timer.schedule): self._timer.current = self._timer.schedule[-1]
            self._timer.setup_time()
        self._timer.circuit_overseer = True
        if self._db.meeting is not None and self._db.meeting.circuit_overseer != True:
            self._db.meeting.circuit_overseer = True
            self._db.meeting.save()

    def normal_mode(self):
        if not self._timer.running:
            self._timer.schedule = convert(get_schedule_data_auto(), self._trans)
            self._timer.current = 0
            self._timer.setup_time()
        self._timer.circuit_overseer = False
        if self._db.meeting is not None and self._db.meeting.circuit_overseer != False:
            self._db.meeting.circuit_overseer = False
            self._db.meeting.save()

    def register(self):
        self.register_endpoints()
        self.register_sockets()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "control", role_required("user", "auth.login", "timer.control")(self.index), methods=["GET"])

    def register_sockets(self):
        self._socketio.on_event("connect", self.connect, namespace=self.NAMESPACE)
        self._socketio.on_event("toggle", self.toggle, namespace=self.NAMESPACE)
        self._socketio.on_event("next", self.next, namespace=self.NAMESPACE)
        self._socketio.on_event("prev", self.prev, namespace=self.NAMESPACE)
        self._socketio.on_event("set_current", self.set_current, namespace=self.NAMESPACE)

    def connect(self):
        self._socketio.emit("connect_event", {
            "timer_started": self._timer.running,
            "schedule": self._timer.schedule,
            "current": self._timer.schedule[self._timer.current]
        }, namespace=self.NAMESPACE)

    def emit_status(self):
        self._socketio.emit("status", {
            "timer_started": self._timer.running,
            "current": self._timer.schedule[self._timer.current]
        }, namespace=self.NAMESPACE)
        self._socketio.emit("status", {
            "timer_started": self._timer.running,
            "current": self._timer.schedule[self._timer.current]
        }, namespace="/webclock")

    def emit_warning(self, message: str):
        self._socketio.emit("warning", {
            "message": message
        },
        namespace=self.NAMESPACE)

    @socket_role_required("user")
    def toggle(self):
        if self._timer.running: self._timer.stop()
        else: self._timer.start()
        self.emit_status()

    @socket_role_required("user")
    def next(self):
        if self._timer.running:
            self.emit_warning("Please make sure the timer is not running!")
        else:
            self._timer.next()
            self.emit_status()

    @socket_role_required("user")
    def prev(self):
        if self._timer.running:
            self.emit_warning("Please make sure the timer is not running!")
        else:
            self._timer.prev()
            self.emit_status()

    @socket_role_required("user")
    def set_current(self, data):
        if self._timer.running: self.emit_warning("Please make sure the timer is not running!")
        index = data["index"]
        self._timer.set_current(index)
        self.emit_status()

    def index(self):
        return render_template("timer/index.html")