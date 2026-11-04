from flask import Blueprint, Flask, render_template
import CLMMobile.utils as utils
from CLMMobile.utils.translation import Translation

class Base:
    def __init__(self, server: Flask, trans: Translation, ip, port):
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
        self._ip = ip
        self._port = port 
        
    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)
        
    def register_endpoints(self):
        self._bp.add_url_rule("/", "base", self.index, methods=["GET"])

    def index(self):
        return render_template("index.html", ip=self._ip, port=self._port, strings=self._trans.get_string_section("base"))