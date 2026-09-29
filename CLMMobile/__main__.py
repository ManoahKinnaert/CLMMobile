from flask import Flask 
from flask_socketio import SocketIO

from CLMMobile.time_service import TimeService
from CLMMobile.time_service.timer import Timer
from CLMMobile.settings_service import SettingsService
from CLMMobile.base import Base
from CLMMobile.webclock_service import WebclockService
from CLMMobile.translation_service import TranslationService
from CLMMobile.data_service import DataService
from CLMMobile.admin_service import AdminService
from CLMMobile.auth_service import get_secret_key, AuthService

server = Flask(__name__, static_folder=None, template_folder=None)
server.secret_key = get_secret_key()
PORT = 5051
socketio = SocketIO(server)
# non-blueprint services
db = DataService()
settings = SettingsService()
trans = TranslationService(settings)
auth = AuthService()
timer = Timer(socketio, db=db)
# init meeting on db
db.init_meeting()
# register blueprints
Base(server, PORT, trans).register()
TimeService(server, socketio, timer, trans, auth).register()
WebclockService(server, socketio, timer, trans).register()
AdminService(server, trans, db, auth).register()

def run_server(debug=False):
    try:
        socketio.run(app=server, debug=debug, port=PORT, host="0.0.0.0") 
    except KeyboardInterrupt:
        db.close()
        auth.close()

if __name__ == "__main__":
    run_server(debug=True)