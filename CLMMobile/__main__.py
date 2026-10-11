from CLMMobile.server import *
from CLMMobile.console_service import startup_view, user_input
import multiprocessing
import subprocess

def run_tui():
    # show starting view in shell
    print(chr(27) + "[2J")
    startup_view(global_ip=BASE.get_ip(), port=PORT)
    while True:
        try:
            if user_input("Enter q to quit program: ").lower() == "q":
                break
        except KeyboardInterrupt:
            break

def run():
    subprocess.run(["cat", "/dev/location", ">", "/dev/null", "&"], capture_output=False)   # for ish, exploit location service on ios to keep running in background
    process = multiprocessing.Process(target=run_server)
    process.start()
    run_tui()
    process.terminate()
    process.join()
    
if __name__ == "__main__":
    run()