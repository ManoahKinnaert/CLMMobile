import urllib.request
import json 
import pathlib
import datetime
import enum 


SOUNDBOX_API_FEED = "https://soundbox.blob.core.windows.net/meeting-feeds/feed.json"
HOME_PATH = pathlib.Path.home().joinpath(".clmtimer")
FEED_PATH =  HOME_PATH.joinpath("feed/meetingfeed.json")

class TalkType(enum.Enum):
    # Treasures from Gods word
    OPENING_COMMENTS = 0
    TREASURES_TALK = 1
    SPIRITUAL_GEMS = 2
    BIBLE_READING = 3
    # apply yourself to the field ministry
    MINISTRY_TALK = 4
    # Living as christians
    LIVING_TALK = 5
    CONGREGATION_BIBLE_STUDY = 6
    CLOSING_COMMENTS = 7

    def __repr__(self):
        return self.name

class Talk:
    def __init__(self, talk_type: TalkType, time_limit: int, num: int=0):
        self.talk_type = talk_type
        self.time_limit = time_limit
        self.num = num

    def __repr__(self):
        return f"TalkType: {self.talk_type} / Time limit: {self.time_limit} min."

    def to_dict(self, trans):
        meeting_codes = trans.get_meeting_codes()
        return {
            "talktype": self.talk_type.__repr__(), 
            "name": f"{meeting_codes[str(self.talk_type.__repr__())]} {self.num if self.num != 0 else ""}", 
            "time": self.time_limit, 
            "num": self.num
        }

def update_schedule_data_auto():
    if not FEED_PATH.parent.exists(): FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(urllib.request.urlopen(SOUNDBOX_API_FEED, timeout=10).read())
        with open(FEED_PATH, "w") as feed:
            json.dump(data, feed, ensure_ascii=False, indent=4)
        return data
    except Exception as e:
        print(f"[ERROR]: Something went wrong with api request: {e}")
        return None

def get_schedule_data_auto():
    # check if meetingfeed.json exists, if not we create it
    if not FEED_PATH.exists(): update_schedule_data_auto()
    # determine the latest meeting day in the feed, so it can be updated if required (therefore avoiding to constantly call the api service)
    with open(FEED_PATH, "r") as feed:
        data = json.load(feed)
    # determine weeknum and year of the current day
    year, weeknum, dayofweek = datetime.datetime.now().isocalendar()
    # determine weeknum and year of the latest meeting in the cached feed
    latest_meeting_date = datetime.datetime.fromisoformat(data[-1]["date"])
    y, wn, _ = latest_meeting_date.isocalendar()
    if year > y or weeknum >= wn: update_schedule_data_auto()
    # now we want todays meeting schedule data 
    relevant = None
    for meeting in data:
        _, week, dow = datetime.datetime.fromisoformat(meeting["date"]).isocalendar()
        if week == weeknum and ((dayofweek < 6 and dow < 6) or dayofweek >= 6): relevant = meeting 
    return relevant["talks"]

def assemble_schedule():
    talks = [
        Talk(TalkType.OPENING_COMMENTS, time_limit=1),
        Talk(TalkType.TREASURES_TALK, time_limit=10),
        Talk(TalkType.SPIRITUAL_GEMS, time_limit=10),
        Talk(TalkType.BIBLE_READING, time_limit=4)
    ]
    remaining = get_schedule_data_auto()
    ministry, living = 1, 1
    for talk in remaining:
        if talk["talkType"] // 100 == 1:
            talks.append(Talk(talk_type=TalkType.MINISTRY_TALK, time_limit=talk["minutes"], num=ministry))
            ministry += 1
        else:
            talks.append(Talk(talk_type=TalkType.LIVING_TALK, time_limit=talk["minutes"], num=living))
            living += 1
    talks.append(Talk(TalkType.CONGREGATION_BIBLE_STUDY, time_limit=30))
    talks.append(Talk(TalkType.CLOSING_COMMENTS, time_limit=3))
    return talks 

if __name__ == "__main__":
    print(assemble_schedule())