from flask import Flask, redirect
from CLMMobile.base import Base 

server = Flask(__name__)

base = Base(server)
base.register()


# automatically redirect to base
@server.route("/")
def main():
    return redirect("base")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5051, debug=True)