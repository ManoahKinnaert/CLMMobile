from peewee import *
import datetime 

DB_PROXY = Proxy()

class BaseModel(Model):
    """
    Base data model
    """
    class Meta:
        database = DB_PROXY

class Meeting(BaseModel):
    """
    Meeting data model
    """
    data = DateField(default=datetime.date.today, index=True, unique=True)


class Talk(BaseModel):
    """
    Talk data model
    """
    meeting = ForeignKeyField(Meeting)
    talk_type = IntegerField()
    measured_time = IntegerField(default=0)
    time_limit = IntegerField(default=0)
    sequence_number = IntegerField(default=0)

    class Meta:
        """
        Primary key represented as a composite key of meeting, talk_type and sequence_number
        """
        primary_key = CompositeKey("meeting", "talk_type", "sequence_number")