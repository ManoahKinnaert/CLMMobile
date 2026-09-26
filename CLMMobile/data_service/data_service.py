from .models import DB_PROXY, Meeting, Talk
from peewee import *
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
        self.db.create_tables([Meeting, Talk])

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

    def get_meetings(self):
        meetings = Meeting.select()
        dates = []
        for meeting in meetings: dates.append(meeting.date)
        return [d.strftime("%d/%m/%Y") for d in dates]

    def get_talks(self, date: str):
        requested_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        return [talk.__data__ for talk in Talk.select().join(Meeting).where(Meeting.date == requested_date)]

    def close(self):
        self.db.close()