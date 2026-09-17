from flask import Flask, Blueprint, render_template
import pathlib 
import socket 
import qrcode
import base64
from io import BytesIO

class Base:
    FILE = pathlib.Path(__file__).resolve().parent.parent

    def __init__(self, app: Flask, port: int):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("base", __name__, 
                            template_folder=str(self.FILE / "assets/templates"),
                            static_folder=str(self.FILE / "assets/static"))

        self._ip = self._get_ip()
        self._local_ip = "127.0.0.1"
        self.port = port
        self.webclock_qr, self.timer_qr = self.generate_qr_codes()
        self.register_endpoints()    

    def register(self):
        self.app.register_blueprint(self.bp)
 
    def register_endpoints(self):
        self.bp.add_url_rule("/", "base", self.base_endpoint, methods=["GET"])

    def _get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(("10.20.30.40", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP 

    def generate_qr_codes(self):
        webclock_adress = f"http://{self._ip}:{self.port}/webclockservice"
        timercontrol_adress = f"http://{self._ip}:{self.port}/timeservice/control"
        webclock_qr = qrcode.make(webclock_adress)
        timer_qr = qrcode.make(timercontrol_adress)
        buff1, buff2 = BytesIO(), BytesIO()
        webclock_qr.save(buff1, format="PNG")
        timer_qr.save(buff2, format="PNG")
        return base64.b64encode(buff1.getvalue()).decode(), base64.b64encode(buff2.getvalue()).decode()

    # endpoints
    def base_endpoint(self):
        return render_template("base/index.html", ip_local=self._local_ip, ip_global=self._ip, port=self.port,
                               webclock_qr=self.webclock_qr, timer_qr=self.timer_qr)