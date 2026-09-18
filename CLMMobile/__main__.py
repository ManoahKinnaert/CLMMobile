from flask import Flask 
from flask_socketio import SocketIO

from time_service import TimeService
from time_service.timer import Timer
from base import Base
from webclock_service import WebclockService
from translation_service import TranslationService
from data_service import DataService
from admin_service import AdminService
from auth_service import get_secret_key

server = Flask(__name__, static_folder=None, template_folder=None)
server.secret_key = get_secret_key()
socketio = SocketIO(server)
db = DataService()
timer = Timer(socketio, db=db)
trans = TranslationService()
PORT = 5051
db.init_meeting()

# register blueprints
Base(server, PORT).register()
TimeService(server, socketio, timer, trans, db).register()
WebclockService(server, socketio, timer, trans).register()
AdminService(server, trans, db).register()

def run_server(debug=False):
    try:
        socketio.run(app=server, debug=debug, port=PORT, host="0.0.0.0") 
    except KeyboardInterrupt:
        db.close()

if __name__ == "__main__":
    run_server(debug=True)