from CLMMobile.utils import DB_PATH
from .models import DB_PROXY, Meeting, Talk 
from peewee import *
import datetime 

class DataService:
    def __init__(self):
        if not DB_PATH.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        self.db = SqliteDatabase(DB_PATH, pragmas={
            "journal_mode": "wal",
            "cache_size": -64000
        })
        DB_PROXY.initialize(self.db)
        self.db.create_tables([Meeting, Talk], safe=True)

        self.meeting: Meeting | None = None 

        if self.db.is_closed(): self.db.connect()

    def init_meeting(self):
        try:
            with self.db.atomic():
                self.meeting, _ = Meeting.get_or_create(
                    date=datetime.date.today()
                )
        except IntegrityError as ie:
            print(f"[ERROR]: DB Integrity error: {ie}")

    def add_talk(self, talk_type: int, measured_time: int, time_limit: int, sequence_number: int=0):
        if self.meeting is None: return 
        try:
            with self.db.atomic():
                talk, created = Talk.get_or_create(
                    meeting=self.meeting,
                    talk_type=talk_type,
                    sequence_number=sequence_number,
                    defaults={
                        "measured_time": measured_time,
                        "time_limit": time_limit
                    }
                ) 
                if not created:
                    talk.measured_time = measured_time 
                    talk.time_limit = time_limit
                    talk.save()
        except IntegrityError as ie:
            print(f"[ERROR]: DB Integrity error: {ie}")
        except Exception as e: print(e)

    def get_meeting_dates(self):
        meetings = Meeting.select()
        return [d.strftime("%d/%m/%Y") for d in (meeting.date for meeting in meetings)]

    def get_meeting_data(self, date: str):
        meeting = Meeting.get_or_none(Meeting.date == datetime.datetime.strptime(date, "%d/%m/%Y").date())
        if meeting is None: return
        return sorted([talk.__data__ for talk in Talk.select().where(Talk.meeting == meeting)], key=lambda k: (k["talk_type"], k["sequence_number"]))

    def close(self):
        self.db.close()