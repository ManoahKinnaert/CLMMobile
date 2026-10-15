from flask import Blueprint, Flask, render_template, url_for
import CLMMobile.utils as utils

class Base:
    def __init__(self, server: Flask):
        """
        Base blueprint template class.
        It takes the Flask server as argument, and adds the relevant endpoints to it.
        """
        self._server: Flask = server 

        self._bp: Blueprint = Blueprint("base",
                                         __name__, 
                                        template_folder=utils.TEMPLATES_DIR,
                                        static_folder=utils.STATIC_DIR,
                                        url_prefix="/base")
        

    def register(self):
        self.register_endpoints()
        self._server.register_blueprint(self._bp)
        

    def register_endpoints(self):
        self._bp.add_url_rule("/", "base", self.index, methods=["GET"])

    def index(self):
        print(url_for("base.static", filename="css/base.css"))
        return render_template("base/index.html")