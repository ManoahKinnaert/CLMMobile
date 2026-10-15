from flask import Flask 
from CLMMobile.base import Base 

server = Flask(__name__)

base = Base(server)
base.register()

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5051, debug=True)