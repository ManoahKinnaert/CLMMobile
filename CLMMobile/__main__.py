from CLMMobile.server import run, run_tui, setup, socketio, server
import subprocess, threading

def run_server():
    try:
        subprocess.Popen(
        ["cat", "/dev/location"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        )   # for ish, exploit location service on ios to keep running in background
    except FileNotFoundError:
        pass

    BASE, trans = setup()

    server_thread = threading.Thread(
        target=lambda: socketio.run(
            app=server, host="0.0.0.0", port=5051,
            debug=True, allow_unsafe_werkzeug=True, use_reloader=False,
        ),
        daemon=True,
    )
    server_thread.start()

    run_tui(trans, BASE)

if __name__ == "__main__":
    run_server()
