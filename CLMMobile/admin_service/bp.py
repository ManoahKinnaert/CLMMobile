from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, Response, send_file
from auth_service import role_required, AuthService
from translation_service import TranslationService
from data_service import DataService
from report_service import Generator
import pathlib

class AdminService:
    FILE = pathlib.Path(__file__).resolve().parent.parent 
    NAMESPACE = "/admin"

    CODE_TABLE = {
                0: "OPENING_COMMENTS",
                1: "TREASURES_TALK",
                2: "SPIRITUAL_GEMS",
                3: "BIBLE_READING",
                4: "MINISTRY_TALK",
                5: "LIVING_TALK",
                6: "CONGREGATION_BIBLE_STUDY",
                7: "CLOSING_COMMENTS",
                8: "PUBLIC_TALK",
                9: "WATCHTOWER_STUDY"
            }

    def __init__(self, app: Flask, trans: TranslationService, dataservice: DataService, auth: AuthService):
        self.app: Flask = app
        self.bp: Blueprint = Blueprint("admin_service", __name__,
                            template_folder=str(self.FILE / "assets/templates"),
                            static_folder=str(self.FILE / "assets/static"),
                            url_prefix=self.NAMESPACE)
        self.trans: TranslationService = trans 
        self.dataservice: DataService = dataservice
        self.auth: AuthService = auth
        self.report_gen: Generator = Generator()
        self.register_endpoints()

    def register(self):
        self.app.register_blueprint(self.bp)

    def _construct_report_data(self, data):
        report_data = {"date": data[0], "pre-talks": [], "meeting-parts": []}
        meeting_codes = self.trans.get_meeting_codes()
        strings = self.trans.get_ui_strings()["admin-dash-reports"]
        for talk in data[1]:
            if talk["talk_type"] == 0:
                report_data["pre-talks"].append({"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                 "time_limit": talk["time_limit"],
                                                 "time_used": talk["measured_time"]})
                report_data["meeting-parts"].append({"name": strings["treasures"], "color": (), "talks": []})
            elif talk["talk_type"] < 3:
                report_data["meeting-parts"][0]["talks"].append(
                    {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                 "time_limit": talk["time_limit"],
                                                 "time_used": talk["measured_time"]}
                )
            elif talk["talk_type"] == 3:
                report_data["meeting-parts"][0]["talks"].append(
                                    {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                                 "time_limit": talk["time_limit"],
                                                                 "time_used": talk["measured_time"]}
                                )
                report_data["meeting-parts"].append({"name": strings["apply-ministry"], "color": (), "talks": []})
            elif talk["talk_type"] < 5:
                report_data["meeting-parts"][1]["talks"].append(
                                                    {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                                                 "time_limit": talk["time_limit"],
                                                                                 "time_used": talk["measured_time"]}
                                                )  
            elif talk["talk_type"] == 6 and talk["sequence_number"] == 0:
                report_data["meeting-parts"].append({"name": strings["living-as-christians"], "color": (), "talks": []})

                report_data["meeting-parts"][2]["talks"].append(
                                                    {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                                                 "time_limit": talk["time_limit"],
                                                                                 "time_used": talk["measured_time"]}
                                                )
            
            elif talk["talk_type"] >= 8:
                report_data["pre-talks"].append( {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                                                                 "time_limit": talk["time_limit"],
                                                                                                 "time_used": talk["measured_time"]})
            else:
                report_data["meeting-parts"][1]["talks"].append(
                                                    {"name": meeting_codes[self.CODE_TABLE[talk["talk_type"]]] + f"{talk['sequence_number'] if talk['sequence_number'] != 0 else ''}",
                                                                                 "time_limit": talk["time_limit"],
                                                                                 "time_used": talk["measured_time"]}
                                                )
        return report_data
        
    def register_endpoints(self):
        self.bp.add_url_rule("/login", "login", self.login, methods=["POST", "GET"])
        self.bp.add_url_rule("/", "dashboard", role_required("admin", "admin_service.login")(self.dashboard), methods=["GET"])
        self.bp.add_url_rule("/reports", "reports", role_required("admin", "admin_service.login")(self.reports_dashboard), methods=["GET"])
        self.bp.add_url_rule("/reports/view", "reports_view", role_required("admin", "admin_service.login")(self.report_view), methods=["GET"])
        self.bp.add_url_rule("/set_language", "set_language", role_required("admin", "admin_service.login")(self.set_language), methods=["POST"])
        self.bp.add_url_rule("/reports/view/download", "download_report", role_required("admin", "admin_service.login")(self.get_report), methods=["GET"])

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
        return render_template("admin_service/reports.html", strings=self.trans.get_ui_strings()["admin-dash-reports"], meetings=self.dataservice.get_meetings())

    def report_view(self):
        date = request.args.get("date")
        data = self.dataservice.get_talks(date)  
        self.report_gen.report_data = self._construct_report_data(data=[date, data])
        #print(self.report_gen.report_data)
        return render_template("admin_service/report_view.html", strings=self.trans.get_ui_strings()["admin-dash-report-view"], date=date, data=data, codes=self.CODE_TABLE, meeting_codes=self.trans.get_meeting_codes())

    def get_report(self):
        self.report_gen.generate()
        pdf_bytes = self.report_gen.get_pdf_bytes()
        self.report_gen.reset()
        return send_file(
            pdf_bytes,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="document.pdf",
    ) 
        
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