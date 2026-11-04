from flask import Flask, Blueprint, render_template, redirect, request, session, url_for
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR
from CLMMobile.utils.translation import Translation
from .db import AuthService
from .auth import ROLES

class AuthBp:

    NAMESPACE = "/auth"

    def __init__(self, server: Flask, trans: Translation):
        self._server: Flask = server 
        self._bp: Blueprint = Blueprint("auth", __name__,
                             template_folder=TEMPLATES_DIR / "auth",
                             static_folder=STATIC_DIR,
                             url_prefix=self.NAMESPACE)
        self._trans: Translation = trans 
        self.auth: AuthService = AuthService()

    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/login", "login", self.login, methods=["POST", "GET"])

    def login(self):
        next_url = request.args.get("next") or request.form.get("next")
        required_role = request.args.get("required_role") or request.form.get("required_role")
        if request.method == "POST":
            password = request.form.get("password", "")
            role = self.auth.verify_passcode(password, required_role)
            if ROLES.get(role, 0) >= ROLES[required_role]:
                session["role"] = role 
                if next_url:
                    return redirect(url_for(next_url))
                return redirect(url_for("base.base"))
            return render_template("auth/index.html",  error=self._trans.get_string_section("auth")["error"], url=url_for("auth.login"), next=next_url, required_role=required_role)
        return render_template("auth/index.html", url=url_for("auth.login"), next=next_url, required_role=required_role)