from flask_socketio import SocketIO
import threading 
import time

class Timer:
    def __init__(self, socketio: SocketIO):
        self.socket: SocketIO = socketio

        self.limit: int = 60
        self.remaining: int = self.limit 
        self.over_time: int = 0
        self.end_time: int = None 
        self.running: bool = False 

        self.lock: threading.Lock = threading.Lock()

        self._schedule: list = None 
        self.current: int = 0

        self.socket.start_background_task(self._run)

    @property
    def schedule(self):
        return self._schedule.copy()

    @schedule.setter
    def schedule(self, new_schedule: list):
        self._schedule = new_schedule.copy()

    def setup_time(self):
        self.limit = self._schedule[self.current]["time"] * 60
        self.remaining = self.limit 
        self.over_time = 0
        self.end_time = None

    def start(self):
        with self.lock:
            if not self.running:
                self.end_time = round(time.monotonic() + self.remaining) if self.end_time is None else self.end_time
                self.running = True 
            
    def stop(self):
        with self.lock:
            emit_data = None 
            if self.running:
                self.remaining = max(0, round(self.end_time - time.monotonic()))
                if self.remaining <= 0: self.over_time = round(time.monotonic() - self.end_time)
                emit_data = (self.remaining, self.over_time)
            self.running = False 
        if emit_data is not None:
            self._emit(emit_data)

        self.next()

    def next(self):
        with self.lock:
            if self.running: return 
            if self.current + 1 < len(self._schedule): self.current += 1 
            else: self.current = 0
            self.setup_time()

    def prev(self):
        with self.lock:
            if self.running: return 
            if self.current - 1 >= 0:
                self.current -= 1
                self.setup_time()

    def set_current(self, index: int):
        with self.lock:
            if index < 0 or index >= len(self._schedule) or self.running: return 
            self.current = index 
            self.setup_time()  

    def _run(self):
        while True:
            emit_data = None 
            with self.lock:
                if self.running:
                    self.remaining = max(0, round(self.end_time - time.monotonic()))
                    if self.remaining <= 0:
                        self.over_time = round(time.monotonic() - self.end_time)
                    emit_data = (self.remaining, self.over_time)
            if emit_data is not None:
                self._emit(emit_data)
            self.socket.sleep(0.1)

    def _emit(self, emit_data):
        remaining, overtime = emit_data 
        # submit control clock data
        self.socket.emit("clockdata", {
            "remaining": remaining,
            "over_time": overtime
        }, namespace="/timer")