from flask import Blueprint, Flask, render_template, url_for
import CLMMobile.utils as utils

class Base:
    def __init__(self, server: Flask, ip, port):
        """
        Base blueprint template class.
        It takes the Flask server as argument, and adds the relevant endpoints to it.
        """
        self._server: Flask = server 

        self._bp: Blueprint = Blueprint("base",
                                         __name__, 
                                        template_folder=utils.TEMPLATES_DIR / "base",
                                        static_folder=utils.STATIC_DIR)
        self._ip = ip
        self._port = port 
        
    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)
        
    def register_endpoints(self):
        self._bp.add_url_rule("/", "base", self.index, methods=["GET"])

    def index(self):
        return render_template("index.html", ip=self._ip, port=self._port)