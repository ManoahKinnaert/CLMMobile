from CLMMobile.server import *
from CLMMobile.console_service import startup_view, user_input
import multiprocessing
import subprocess

def run_tui(window=None):
    # show starting view in shell
    print(chr(27) + "[2J")
    startup_view(global_ip=BASE.get_ip(), port=PORT)
    while True:
        try:
            if user_input("Enter q to quit program: ").lower() == "q":
                break
        except Exception:
            break
    if window:
        window.destroy()


def on_win_close(process):
    import os
    process.kill()
    os._exit(0)

def run():
    process = multiprocessing.Process(target=run_server)
    process.start()
    try:
        import webview
        window = webview.create_window("CLMMobile", url=f"http://{BASE.get_ip()}:{PORT}")
        window.events.closing += lambda: on_win_close(process)
        webview.start(run_tui, window)
        process.terminate()
        process.join()
    except:
        subprocess.run(["cat", "/dev/location", "&"])   # for ish
        run_tui()
    
if __name__ == "__main__":
    run()