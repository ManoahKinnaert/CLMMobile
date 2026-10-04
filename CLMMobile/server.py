from flask import Flask, render_template 
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
socketio = SocketIO(server, async_mode="gevent")
# non-blueprint services
db = DataService()
settings = SettingsService()
trans = TranslationService(settings)
auth = AuthService()
timer = Timer(socketio, db=db)
# init meeting on db
db.init_meeting()
# register blueprints
BASE = Base(server, PORT, trans)
BASE.register()
TimeService(server, socketio, timer, trans, auth).register()
WebclockService(server, socketio, timer, trans).register()
AdminService(server, trans, db, auth).register()

# set basic 404 and 500 screens
@server.errorhandler(404)
def handle_404(_):
    return render_template("base/404.html"), 404

@server.errorhandler(500)
def handle_500(_):
    return render_template("base/500.html"), 500

def run_server(debug=False):
    try:
        socketio.run(app=server, debug=debug, port=PORT, host="0.0.0.0", allow_unsafe_werkzeug=True) 
    except KeyboardInterrupt:
        db.close()
        auth.close()
