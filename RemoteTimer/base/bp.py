from flask import Flask, Blueprint, render_template
import pathlib 

class Base:
    FILE = pathlib.Path(__file__).resolve().parent

    def __init__(self, app: Flask):
        self.app: Flask = app 
        self.bp: Blueprint = Blueprint("base", __name__, 
                            template_folder=str(self.FILE / "./templates"),
                            static_folder=str(self.FILE.parent / "./assets"))

        self.register_endpoints()    

    def register(self):
        self.app.register_blueprint(self.bp)
 
    def register_endpoints(self):
            self.bp.add_url_rule("/", "base", self.base_endpoint, methods=["GET"])
    
    # endpoints and websocket stuff
    def base_endpoint(self):
        return render_template("base.html")