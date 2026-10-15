from flask import Flask, redirect
from CLMMobile.base import Base 
from CLMMobile.utils import TEMPLATES_DIR, STATIC_DIR

server = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)

base = Base(server)
base.register()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5051, debug=True)