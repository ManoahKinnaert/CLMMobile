from flask import Blueprint, Flask, render_template
import CLMMobile.utils as utils
from CLMMobile.utils.data import DataService
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import role_required, socket_role_required

class AdminBp:
    NAMESPACE = "/admin"
    def __init__(self, server: Flask, trans: Translation, db: DataService):
        self._server: Flask = server
        self._bp: Blueprint = Blueprint("admin",
                                        __name__,
                                        template_folder=utils.TEMPLATES_DIR / "admin",
                                        static_folder=utils.STATIC_DIR,
                                        url_prefix=self.NAMESPACE)
        self._trans: Translation = trans 
        self._db: DataService = db

    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "dash", role_required("admin", "auth.login", "admin.dash")(self.dashboard), methods=["GET"])

    def dashboard(self):
        return render_template("admin/index.html")