from CLMMobile.server import run_tui, setup, socketio, server, _silence_dev_server, PORT
import subprocess
import threading


def run_server():
    _silence_dev_server()

    try:
        subprocess.Popen(
            ["cat", "/dev/location"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except FileNotFoundError:
        pass

    BASE, trans = setup()

    server_thread = threading.Thread(
        target=lambda: socketio.run(
            app=server,
            host="0.0.0.0",
            port=PORT,
            debug=False,
            allow_unsafe_werkzeug=True,
            use_reloader=False
        ),
        daemon=True
    )

    server_thread.start()

    run_tui(trans, BASE)


if __name__ == "__main__":
    run_server()
