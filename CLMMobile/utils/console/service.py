from .constants import *
import os, re

# basic rendering functions
def render_title_logo():
    print(f"{BOLD}{LOGO}{RESET}\n")

def render_separator():
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    print(f"{DIM}{'─' * min(columns, 90)}{RESET}")

def render_markdown(markdown: str):
    print(re.sub(r"\*\*(.+?)\*\*", rf"{BOLD}\1{RESET}", markdown))

def user_input(message: str=""):
    render_separator()
    user_input = input(f"{BOLD}{GREEN}{message} ❯{RESET} ").strip()
    render_separator()
    return user_input

def startup_view(strings, global_ip, port):
    render_title_logo()
    render_separator()
    render_markdown(f"{GREEN}**{strings["running"]}**\n{RESET}")
    render_markdown(f"{YELLOW}{strings["local"]}: **http://127.0.0.1:{port}/**\n{RESET}")
    render_markdown(f"{YELLOW}{strings["global"]}: **http://{global_ip}:{port}/**\n{RESET}")
    