from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
from CLMMobile.utils import AUTH_DB

DB_PROXY = Proxy()

class AuthService:
    class Credential(Model):
        role = CharField(unique=True)   # user or admin
        passcode_hash = CharField()

        class Meta:
            database = DB_PROXY

    def __init__(self):
        if not AUTH_DB.exists():
            self._create_auth_db()
        else:
            self.db = SqliteDatabase(AUTH_DB)
            DB_PROXY.initialize(self.db)

        if self.db.is_closed(): self.db.connect()

    def _create_auth_db(self):
        AUTH_DB.touch(exist_ok=True)
        self.db = SqliteDatabase(AUTH_DB)
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