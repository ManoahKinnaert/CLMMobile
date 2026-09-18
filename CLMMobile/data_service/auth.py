from functools import wraps
from flask import session, redirect, url_for
import secrets
import pathlib

SECRET_KEY_PATH = pathlib.Path.home() / ".clmtimer" / ".secret_key"
ROLE_LEVELS = {"user": 1, "admin": 2}

def _has_role(min_role):
    user_role = session.get("role")
    return bool(user_role) and ROLE_LEVELS.get(user_role, 0) >= ROLE_LEVELS[min_role]

def role_required(min_role):
    # redirect to login if needed
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not _has_role(min_role):
                return redirect(url_for("time_service.login"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def socket_role_required(min_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, *args, **kwargs):
            if not _has_role(min_role):
                return False  # no-op for normal events, refuses handshake for connect
            return fn(self, *args, **kwargs)
        return wrapper
    return decorator

def get_secret_key():
    # gets the app secret key and generates one if it isnt set
    if SECRET_KEY_PATH.exists():
        return SECRET_KEY_PATH.read_text().strip()

    SECRET_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32)
    SECRET_KEY_PATH.write_text(key)
    return key