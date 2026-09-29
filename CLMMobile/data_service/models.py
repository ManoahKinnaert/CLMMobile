from peewee import *
import datetime 

DB_PROXY = Proxy()

class BaseModel(Model):
    """
    Base data model.
    """
    class Meta:
        database = DB_PROXY

class Meeting(BaseModel):
    """
    Meeting data model.
    """
    date = DateField(default=datetime.date.today, index=True, unique=True)          # the date of the meeting

class Talk(BaseModel):
    """
    Talk data model.
    """
    meeting = ForeignKeyField(Meeting)      # the meeting where this talk belongs to -> foreignkey
    talk_type = IntegerField()              # the talk type represented as an int -> see schedule_service for more info              
    meeting_section = IntegerField()        # the meeting section represented as an int -> see schedule_service for more info
    measured_time = IntegerField()          # the measured time of the talk in seconds
    time_limit = IntegerField()             # the time limit of the talk in minutes
    sequence_number = IntegerField()        # the 'count' of the talk (so if this is the first, second, third, ect. talk with this talk type)
    
    class Meta:
        """
        Primary key represented as a composite key of talk_type and sequence_number
        """
        primary_key = CompositeKey('talk_type', 'sequence_number')
