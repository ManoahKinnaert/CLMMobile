from flask import Blueprint, Flask, render_template, request, Response
import CLMMobile.utils as utils
from CLMMobile.utils.data import DataService
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth import role_required, socket_role_required

class AdminBp:
    NAMESPACE = "/admin"
    def __init__(self, server: Flask, trans: Translation, auth, db: DataService):
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
        self._bp.add_url_rule("/set_lang", "set_lang", role_required("admin", "auth.login", "admin.set_lang")(self.set_lang), methods=["POST"])
        self._bp.add_url_rule("/user_pass", "set_user_pass", role_required("admin", "auth.login", "admin.set_user_pass")(self.set_user_pass), methods=["POST"])
        self._bp.add_url_rule("/admin_pass", "set_admin_pass", role_required("admin", "auth.login", "admin.set_admin_pass")(self.set_admin_pass), methods=["POST"])

    def set_lang(self):
        try:
            data = request.get_json(silent=True)
            if not data or "language" not in data:
                return {"error": "Missing 'lang' in request body"}, 400

            lang = data["language"]
            if not isinstance(lang, str) or not lang.strip():
                return {"error": "'language' must be a non-empty string"}, 400

            if lang not in self._trans.get_languages():
                return {"error": "Unsupported language:" + lang}, 400

            self._trans.language = lang 
            return Response(status=200)
        except (TypeError, KeyError, ValueError):
            return Response(status=400)
        except Exception as e:
            print(e)
            return Response(status=500)

    def set_user_pass(self):
        try:
            user_pass = request.get_json()["user_password"]
            pass 
        except:
            pass 

    def set_admin_pass(self):
        pass 

    def dashboard(self):
        return render_template("admin/index.html", current_lang=self._trans.language, langs=self._trans.get_languages(), strings=self._trans.get_string_section("admin"))