from flask import Blueprint, Flask, render_template
import CLMMobile.utils as utils

class Base:
    def __init__(self, server: Flask):
        self._server: Flask = server 

        self._bp: Blueprint = Blueprint("base", __name__, template_folder=utils.TEMPLATES_DIR,
                             static_folder=utils.STATIC_DIR)

        
    