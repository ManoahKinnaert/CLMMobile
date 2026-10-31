from flask import Flask, Blueprint, render_template, redirect, request, session, url_for
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR
from .db import AuthService

class AuthBp:

    NAMESPACE = "/auth"

    def __init__(self, server: Flask):
        self._server: Flask = server 
        self._bp: Blueprint = Blueprint("auth", __name__,
                             template_folder=TEMPLATES_DIR / "auth",
                             static_folder=STATIC_DIR,
                             url_prefix=self.NAMESPACE)

        self.auth: AuthService = AuthService()

    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/login", "login", self.login, methods=["POST", "GET"])

    def login(self):
        next_url = request.args.get("next") or request.form.get("next")
        if request.method == "POST":
            password = request.form.get("password", "")
            role = self.auth.verify_passcode(password)
            if role:
                session["role"] = role 
                if next_url:
                    return redirect(url_for(next_url))
                return redirect(url_for("base.base"))
            return render_template("auth/index.html",  error="Wrong password!", url=url_for("auth.login"), next=next_url)
        return render_template("auth/index.html", url=url_for("auth.login"), next=next_url)