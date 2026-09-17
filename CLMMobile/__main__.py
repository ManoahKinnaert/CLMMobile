from flask import Flask 
from flask_socketio import SocketIO

from time_service import TimeService
from base import Base
from webclock_service import WebclockService

server = Flask(__name__)
socketio = SocketIO(server)
PORT = 5051

# register blueprints
Base(server, PORT).register()
TimeService(server, socketio).register()
WebclockService(server, socketio).register()

def run_server(debug=False, globaly=False):
    socketio.run(app=server, debug=debug, port=PORT, host="127.0.0.1" if not globaly else "0.0.0.0") 

if __name__ == "__main__":
    run_server(debug=True, globaly=False)