from .constants import *
import os, re

# basic rendering functions
def render_title_logo():
    print(f"{BOLD}{LOGO}{RESET}\n")

def render_seperator():
    print(f"{DIM}{'─' * min(os.get_terminal_size().columns, 90)}{RESET}")

def render_markdown(markdown: str):
    print(re.sub(r"\*\*(.+?)\*\*", rf"{BOLD}\1{RESET}", markdown))

# TODO: View functions