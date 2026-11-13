from flask import Blueprint, Flask, render_template
import CLMMobile.utils as utils
from CLMMobile.utils.translation import Translation
from io import BytesIO
import socket
import qrcode, base64


class Base:
    def __init__(self, server: Flask, trans: Translation, port):
        """
        Base blueprint template class.
        It takes the Flask server as argument, and adds the relevant endpoints to it.
        """
        self._server: Flask = server 

        self._bp: Blueprint = Blueprint("base",
                                         __name__, 
                                        template_folder=utils.TEMPLATES_DIR / "base",
                                        static_folder=utils.STATIC_DIR)
        self._trans: Translation = trans
        self._ip = self.get_ip()
        self._port = port 

        self.webclock_qr, self.timer_qr, self.admin_qr = self.generate_qr_codes()
        
    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)
        
    def register_endpoints(self):
        self._bp.add_url_rule("/", "base", self.index, methods=["GET"])

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(("10.20.30.40", 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def refresh_ip(self):
        self._ip = self.get_ip()

    def generate_qr_codes(self):
        self.refresh_ip()
        webclock_qr = qrcode.make(f"http://{self._ip}:{self._port}/webclock")
        timer_qr = qrcode.make(f"http://{self._ip}:{self._port}/timer")
        admin_qr = qrcode.make(f"http://{self._ip}:{self._port}/admin")
        bf = BytesIO(), BytesIO(), BytesIO()
        webclock_qr.save(bf[0], format="PNG")
        timer_qr.save(bf[1], format="PNG")
        admin_qr.save(bf[2], format="PNG")
        return base64.b64encode(bf[0].getvalue()).decode(), base64.b64encode(bf[1].getvalue()).decode(), base64.b64encode(bf[2].getvalue()).decode()

    def index(self):
        return render_template("index.html", ip=self._ip, port=self._port, strings=self._trans.get_string_section("base"),
                               webclock_qr=self.webclock_qr, timer_qr=self.timer_qr, admin_qr=self.admin_qr)