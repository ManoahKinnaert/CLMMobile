from functools import wraps
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import *
import pathlib
import secrets

ROLE_LEVELS = {"user": 1, "admin": 2}
DB_PROXY = Proxy()

def _has_role(min_role):
    user_role = session.get("role")
    return bool(user_role) and ROLE_LEVELS.get(user_role, 0) >= ROLE_LEVELS[min_role]

def role_required(min_role, redirect_url: str):
    # redirect to login if needed
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not _has_role(min_role):
                return redirect(url_for(redirect_url))
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
    return secrets.token_hex(16)

class AuthService:
    HOME_PATH = pathlib.Path.home().joinpath(".clmmobile")
    AUTH_DB = HOME_PATH.joinpath(".auth.db")

    class Credential(Model):
        role = CharField(unique=True)   # user or admin
        passcode_hash = CharField()

        class Meta:
            database = DB_PROXY

    def __init__(self):
        if not self.AUTH_DB.exists():
            self._create_auth_db()
        else:
            self.db = SqliteDatabase(self.AUTH_DB)
            DB_PROXY.initialize(self.db)

        if self.db.is_closed(): self.db.connect()

    def _create_auth_db(self):
        self.AUTH_DB.touch(exist_ok=True)
        self.db = SqliteDatabase(self.AUTH_DB)
        DB_PROXY.initialize(self.db)
        self.db.create_tables([self.Credential])
        self.setup_default_passcodes()

    def setup_default_passcodes(self):
        self.set_passcode("admin", "admin")
        self.set_passcode("user", "user")

    def set_passcode(self, role: str, passcode: str):
        hashed = generate_password_hash(passcode)
        try:
            with self.db.atomic():
                self.Credential.insert(role=role, passcode_hash=hashed).on_conflict(
                        conflict_target=[self.Credential.role],
                        update={self.Credential.passcode_hash: hashed}
                    ).execute()
        except IntegrityError:
            print("[ERROR]: DB Integrity error")

    def verify_passcode(self, passcode: str):
        # return matching role ('user' or 'admin') if passcode matches otherwise None
        for cred in self.Credential.select():
            if check_password_hash(cred.passcode_hash, passcode):
                return cred.role
        return None

    def close(self):
        self.db.close()