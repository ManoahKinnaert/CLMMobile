from flask import Blueprint, Flask, render_template, request, Response, redirect, url_for
import CLMMobile.utils as utils
from CLMMobile.utils.data import DataService
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.auth.db import AuthService
from CLMMobile.utils.auth import role_required
from CLMMobile.utils.reports.generator import Generator

class AdminBp:
    NAMESPACE = "/admin"
    def __init__(self, server: Flask, trans: Translation, auth, db: DataService):
        self._server: Flask = server
        self._bp: Blueprint = Blueprint("admin",
                                        __name__,
                                        template_folder=utils.TEMPLATES_DIR / "admin",
                                        static_folder=utils.STATIC_DIR,
                                        url_prefix=self.NAMESPACE)
        self._auth: AuthService = auth
        self._trans: Translation = trans 
        self._db: DataService = db

    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)

    def register_endpoints(self):
        self._bp.add_url_rule("/", "dash", role_required("admin", "auth.login", "admin.dash")(self.dashboard), methods=["GET"])
        self._bp.add_url_rule("/meetings", "meetings", role_required("admin", "auth.login", "admin.meetings")(self.meetings), methods=["GET"])
        self._bp.add_url_rule("/meetings/report", "report", role_required("admin", "auth.login", "admin.report")(self.report), methods=["GET"])
        self._bp.add_url_rule("/meetings/report/download", "report_download", role_required("admin", "auth.login", "admin.report_download")(self.report_download), methods=["GET"])
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
            self._auth.set_passcode(role="user", passcode=user_pass)
        except (TypeError, KeyError, ValueError):
            return Response(status=400)
        except Exception:
            return Response(status=500)

    def set_admin_pass(self):
        try:
            admin_pass = request.get_json()["admin_password"]
            self._auth.set_passcode(role="admin", passcode=admin_pass)
        except (TypeError, KeyError, ValueError):
            return Response(status=400)
        except Exception:
            return Response(status=500)

    def dashboard(self):
        return render_template("admin/index.html", current_lang=self._trans.language, langs=self._trans.get_languages(), strings=self._trans.get_string_section("admin"))

    def meetings(self):
        return render_template("admin/meetings.html", dates=self._db.get_meeting_dates())

    def report(self):
        date = request.args.get("date")
        if date is None:
            return redirect(url_for("admin.meetings"))
        meeting_data = self._db.get_meeting_data(date)
        if meeting_data is None:
            return redirect(url_for("admin.meetings"))

        talk_strings = self._trans.get_string_section("talks") or {}
        sections = {}
        for talk in meeting_data:
            talk_type = talk.get("talk_type")
            section = None
            talk_name = str(talk_type)
            if talk_type is not None:
                for s, rng in Generator.SECTION_RANGES.items():
                    if talk_type in rng:
                        section = s
                        keys = Generator.TALK_NAME_KEYS.get(s, [])
                        index = talk_type - rng.start
                        if 0 <= index < len(keys):
                            talk_name = talk_strings.get(keys[index], keys[index])
                        break
            if section:
                talk["_section"] = section
                talk["_name"] = talk_name
                talk["_time_str"] = f"{talk.get('measured_time', 0) // 60:02d}:{talk.get('measured_time', 0) % 60:02d}"
                talk["_limit_str"] = f"{talk.get('time_limit', 0) // 60:02d}:00"
                sections.setdefault(section, []).append(talk)

        section_order = list(Generator.SECTION_RANGES.keys())
        section_colors = Generator.COLOR_TABLE

        return render_template(
            "admin/report.html",
            date=date,
            sections=sections,
            section_order=section_order,
            talk_strings=talk_strings,
            section_colors=section_colors
        )

    def report_download(self):
        date = request.args.get("date")
        if date is None:
            return redirect(url_for("admin.meetings"))
        meeting_data = self._db.get_meeting_data(date)
        if meeting_data is None:
            return redirect(url_for("admin.meetings"))

        gen = Generator(self._trans, {"date": date, "talks": meeting_data})
        gen.generate()
        pdf_bytes = gen.get_pdf_bytes().read()

        return Response(
            pdf_bytes,
            mimetype="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="report-{date}.pdf"'}
        )