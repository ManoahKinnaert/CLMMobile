from flask import Flask 
from flask_socketio import SocketIO

from time_service import TimeService
from time_service.timer import Timer
from base import Base
from webclock_service import WebclockService
from translation_service import TranslationService

server = Flask(__name__, static_folder=None, template_folder=None)
socketio = SocketIO(server)
timer = Timer(socketio)
trans = TranslationService()
PORT = 5051

# register blueprints
Base(server, PORT).register()
TimeService(server, socketio, timer, trans).register()
WebclockService(server, socketio, timer, trans).register()

def run_server(debug=False):
    socketio.run(app=server, debug=debug, port=PORT, host="0.0.0.0") 

if __name__ == "__main__":
    run_server(debug=True)