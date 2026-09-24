from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, Response
from auth_service import role_required, AuthService
from translation_service import TranslationService
from data_service import DataService
import pathlib

class AdminService:
    FILE = pathlib.Path(__file__).resolve().parent.parent 
    NAMESPACE = "/admin"

    def __init__(self, app: Flask, trans: TranslationService, dataservice: DataService, auth: AuthService):
        self.app: Flask = app
        self.bp: Blueprint = Blueprint("admin_service", __name__,
                            template_folder=str(self.FILE / "assets/templates"),
                            static_folder=str(self.FILE / "assets/static"),
                            url_prefix=self.NAMESPACE)
        self.trans: TranslationService = trans 
        self.dataservice: DataService = dataservice
        self.auth: AuthService = auth

        self.register_endpoints()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/login", "login", self.login, methods=["POST", "GET"])
        self.bp.add_url_rule("/", "dashboard", role_required("admin", "admin_service.login")(self.dashboard), methods=["GET"])
        self.bp.add_url_rule("/reports", "reports", role_required("admin", 'admin_service.login')(self.reports_dashboard), methods=["GET"])
        self.bp.add_url_rule("/set_language", "set_language", role_required("admin", "admin_service.login")(self.set_language), methods=["POST"])

    def login(self):
        if request.method == "POST":
            passcode = request.form.get("passcode", "")
            role = self.auth.verify_passcode(passcode)
            if role:
                session["role"] = role
                return redirect(url_for("admin_service.dashboard"))
            return render_template("auth_service/login.html", error="Invalid passcode", form_title="Login - Admin", url=url_for("admin_service.login"))

        return render_template("auth_service/login.html", error=None, form_title="Login - Admin", url=url_for("admin_service.login")) 

    def dashboard(self):
        return render_template("admin_service/index.html", langs=self.trans.get_languages(), current_lang=self.trans.language, strings=self.trans.get_ui_strings()["admin-dash"])

    def reports_dashboard(self):
        return render_template("admin_service/reports.html", strings=self.trans.get_ui_strings()["admin-dash-reports"])

    def set_language(self):
        data = request.get_json(silent=True)
        if not data or "language" not in data:
            return {"error": "Missing 'lang' in request body"}, 400

        lang = data["language"]
        if not isinstance(lang, str) or not lang.strip():
            return {"error": "'language' must be a non-empty string"}, 400

        if lang not in self.trans.get_languages():
            return {"error": f"Unsupported language: {lang}"}, 400

        self.trans.language = lang
        return Response(status=200)