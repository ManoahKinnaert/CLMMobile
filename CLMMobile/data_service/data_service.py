from data_service.models import DB_PROXY, Meeting, MeetingSection, Talk
from peewee import *
import pathlib
import datetime

class DataService:
    HOME_PATH = pathlib.Path.home().joinpath(".clmmobile")
    DB_PATH =  HOME_PATH.joinpath("db/database.db")

    _SECTION_TABLE = [
        "INTRO", 
        "TREASURES_FROM_GODS_WORD", 
        "APPLY_YOURSELF_TO_THE_FIELDMINISTRY", 
        "LIVING_AS_CHRISTIANS",
        "WEEKEND"
    ]

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
        self.db.create_tables([Meeting, Talk, MeetingSection])

    def init_meeting(self):
        try:
            with self.db.atomic():
                # we overwrite the meeting if it already exists for this date (being today)
                self.meeting, _ = Meeting.get_or_create(
                    date=datetime.date.today()
                )
        except IntegrityError:
            print("[ERROR]: DB Integrity error")

    def add_talk(self, talk_type, meeting_section: int, time: int, time_limit: int, seq_num: int=0):
        if self.meeting is None: print("[ERROR]: meeting is None"); return
        try:
            with self.db.atomic():
                section, _ = MeetingSection.get_or_create(
                    meeting=self.meeting,
                    section_type = meeting_section
                )
                Talk.get_or_create(
                    meeting_section=section,
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

    def _get_meeting_sections(self, date: str):
        requested_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        return [section for section in MeetingSection.select().join(Meeting).where(Meeting.date == requested_date)]

    # TODO: Implement 'custom' section table for some custom meeting schedules
    def get_meeting_data(self, date: str, section_table: list=None):
        sections = self._get_meeting_sections(date)
        data = {"date": date, "meeting-sections": {}}
        print(sections)
        for section in sections:
            talks = [talk.__data__ for talk in Talk.select().join(MeetingSection).where(Talk.meeting_section == section)]
            for t in talks: t["meeting_section"] = section.section_type
            data["meeting-sections"][self._SECTION_TABLE[section.section_type]] = talks
        return data 

    def close(self):
        self.db.close()