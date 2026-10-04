from CLMMobile.server import *
import multiprocessing
import subprocess

def run():
    process = multiprocessing.Process(target=run_server)
    process.start()
    try:
        import webview
        webview.create_window("CLMMobile", url=f"http://{BASE.get_ip()}:{PORT}")
        
        webview.start()
        process.terminate()
        process.join()
    except:
        subprocess.run(["cat", "/dev/location", "&"])   # for ish
        print("Running the server!")

if __name__ == "__main__":
    run()