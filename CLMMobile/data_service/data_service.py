from .models import DB_PROXY, Meeting, Talk, Credential
from peewee import *
from werkzeug.security import generate_password_hash, check_password_hash
import pathlib
import datetime

class DataService:
    HOME_PATH = pathlib.Path.home().joinpath(".clmtimer")
    DB_PATH =  HOME_PATH.joinpath("db/database.db")

    def __init__(self):
        # check if the DB exists, if it doesnt we want to create it
        self.db: SqliteDatabase | None = None
        if not self.DB_PATH.exists():
            self._create_db() 
        else:
            self.db = SqliteDatabase(self.DB_PATH)
            DB_PROXY.initialize(self.db)

        self.meeting: Meeting | None = None

        if self.db.is_closed(): self.db.connect()

    def _create_db(self):
        # create the DB path
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.db = SqliteDatabase(self.DB_PATH, pragmas={
            "journal_mode": "wal",
            "cache_size": -64000
        })
        DB_PROXY.initialize(self.db)
        # we also want to create all relevant tables
        self.db.create_tables([Meeting, Talk, Credential])
        # setup basic starter passwords, recommended to change later...
        self.set_passcode("admin", "admin")
        self.set_passcode("user", "user")

    def init_meeting(self):
        try:
            with self.db.atomic():
                # we overwrite the meeting if it already exists for this date (being today)
                self.meeting, _ = Meeting.get_or_create(
                    date=datetime.date.today()
                )
        except IntegrityError:
            print("[ERROR]: DB Integrity error")

    def add_talk(self, talk_type, time: int, time_limit: int, seq_num: int=0):
        if self.meeting is None: print("[ERROR]: meeting is None"); return
        try:
            with self.db.atomic():
                Talk.get_or_create(
                    meeting=self.meeting,
                    talk_type=talk_type,
                    measured_time=time,
                    time_limit=time_limit,
                    sequence_number=seq_num
                )
        except IntegrityError:
            print("[ERROR]: DB Integrity error")

    def set_passcode(self, role: str, passcode: str):
        hashed = generate_password_hash(passcode)
        try:
            with self.db.atomic():
                Credential.insert(role=role, passcode_hash=hashed).on_conflict(
                    conflict_target=[Credential.role],
                    update={Credential.passcode_hash: hashed}
                ).execute()
        except IntegrityError:
            print("[ERROR]: DB Integrity error")

    def verify_passcode(self, passcode: str):
        # return matching role ('user' or 'admin') if passcode matches otherwise None
        for cred in Credential.select():
            if check_password_hash(cred.passcode_hash, passcode):
                return cred.role
        return None

    def close(self):
        self.db.close()