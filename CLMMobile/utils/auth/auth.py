from functools import wraps 
from flask import session, redirect, url_for 
import os
import secrets 

ROLES = {"user": 1, "admin": 2}

def _has_role(min_role):
    user_role = session.get("role")
    return bool(user_role) and ROLES.get(user_role, 0) >= ROLES[min_role]

def role_required(min_role, redirect_url: str, main_point: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not _has_role(min_role):
                return redirect(url_for(redirect_url, next=main_point))
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
    return os.environ.get("SECRET_KEY") or secrets.token_hex(16)
