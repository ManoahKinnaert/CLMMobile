from .constants import *
import os, re

# basic rendering functions
def render_title_logo():
    print(f"{BOLD}{LOGO}{RESET}\n")

def render_separator():
    print(f"{DIM}{'─' * min(os.get_terminal_size().columns, 90)}{RESET}")

def render_markdown(markdown: str):
    print(re.sub(r"\*\*(.+?)\*\*", rf"{BOLD}\1{RESET}", markdown))

def user_input(message: str=""):
    render_separator()
    user_input = input(f"{BOLD}{GREEN}{message} ❯{RESET} ").strip()
    render_separator()
    return user_input

def startup_view(global_ip, port):
    render_title_logo()
    render_separator()
    render_markdown(f"{GREEN}**Server is running**\n{RESET}")
    render_markdown(f"{YELLOW}Running at: **http://{global_ip}:{port}/**\n{RESET}")
