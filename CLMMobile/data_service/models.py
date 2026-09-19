from peewee import *
import datetime 

DB_PROXY = Proxy()

class BaseModel(Model):
    class Meta:
        database = DB_PROXY

class Meeting(BaseModel):
    date = DateField(default=datetime.date.today, index=True, unique=True) 

class Talk(BaseModel):
    meeting = ForeignKeyField(Meeting) 
    talk_type = IntegerField()
    measured_time = IntegerField()  # in seconds
    time_limit = IntegerField() # in minutes
    sequence_number = IntegerField()
