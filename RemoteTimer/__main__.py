from flask import Flask 
from flask_socketio import SocketIO

from time_service import TimeService
from base import Base

server = Flask(__name__)
socketio = SocketIO(server)
PORT = 5051

# register blueprints
time_service = TimeService(server, socketio)
time_service.register()

base_service = Base(server, PORT)
base_service.register()

def run_server(debug=False, globaly=False):
    socketio.run(app=server, debug=debug, port=PORT, host="127.0.0.1" if not globaly else "0.0.0.0") 

if __name__ == "__main__":
    run_server(debug=True, globaly=True)