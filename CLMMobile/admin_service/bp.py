from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from auth_service import role_required
import pathlib

class AdminService:
    FILE = pathlib.Path(__file__).resolve().parent.parent 
    NAMESPACE = "/admin"

    def __init__(self, app: Flask, trans, dataservice):
        self.app: Flask = app
        self.bp: Blueprint = Blueprint("admin_service", __name__,
                            template_folder=str(self.FILE / "assets/templates"),
                            static_folder=str(self.FILE / "assets/static"),
                            url_prefix=self.NAMESPACE)
        self.trans = trans 
        self.dataservice = dataservice

        self.register_endpoints()

    def register(self):
        self.app.register_blueprint(self.bp)

    def register_endpoints(self):
        self.bp.add_url_rule("/login", "login", self.login, methods=["POST", "GET"])
        self.bp.add_url_rule("/", "dashboard", role_required("admin", "admin_service.login")(self.dashboard), methods=["GET"])

    def login(self):
        if request.method == "POST":
            passcode = request.form.get("passcode", "")
            role = self.dataservice.verify_passcode(passcode)
            if role:
                session["role"] = role
                return redirect(url_for("admin_service.dashboard"))
            return render_template("auth_service/login.html", error="Invalid passcode", form_title="Login - Admin", url=url_for("admin_service.login"))

        return render_template("auth_service/login.html", error=None, form_title="Login - Admin", url=url_for("admin_service.login")) 

    def dashboard(self):
        return render_template("admin_service/index.html")