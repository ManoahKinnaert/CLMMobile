from flask_socketio import SocketIO
import threading
import time 

from .schedule_service import assemble_schedule

class Timer:
    def __init__(self, socketio, limit: int=1):
        self.socket = socketio 

        self.limit: int = 60 * limit 
        self.remaining: int = self.limit
        self.over_time: int = 0
        self.end_time = None 
        self.running = False

        self.lock = threading.Lock()

        self.socket.start_background_task(self._run)

        self.schedule = assemble_schedule()
        self.current = 0

    def setup_time(self):
        self.limit = self.schedule[self.current].time_limit * 60
        self.remaining = self.limit
        self.over_time = 0
        self.end_time = None

    def start(self):
        with self.lock:
            if not self.running:
                self.end_time = round(time.monotonic() + self.remaining) if self.end_time is None else self.end_time
                self.running = True 

    def reset(self):
        with self.lock:
            self.remaining = self.limit
            self.running = False 
            self.end_time = None

        self.setup_time()

    def stop(self):
        with self.lock:
            if self.running:
                self.remaining = max(0, round(self.end_time - time.monotonic()))
                if self.remaining <= 0: self.over_time = round(time.monotonic() - self.end_time)
            self.running = False 
        self._emit()
        # TODO: Save the data to a database
        # go to the next talk unless this was the last one, if it is the last one we revert to the first talk
        self.next()

    def next(self):
        if self.running: return
        if self.current + 1 < len(self.schedule): self.current += 1
        else: self.current = 0
        self.setup_time() 

    def prev(self):
        if self.running: return
        if self.current - 1 >= 0: 
            self.current -= 1
            self.setup_time()

    def set_current(self, index: int):
        if index < 0 or index >= len(self.schedule): return 
        self.current = index 
        self.setup_time()

    def _run(self):
        while True:
            with self.lock:
                if self.running:
                    self.remaining = max(0, round(self.end_time - time.monotonic()))

            if self.running:
                self._emit()
                if self.remaining <= 0:
                    self.over_time = round(time.monotonic() - self.end_time)

            self.socket.sleep(0.2)

    def _emit(self):
        # submit webclock data
        self.socket.emit("webclockdata", {"remaining": self.remaining, "over_time": self.over_time}, namespace="/webclockservice")
        # submit control clock data
        self.socket.emit("clockdata", {"remaining": self.remaining, "over_time": self.over_time}, namespace="/timeservice")