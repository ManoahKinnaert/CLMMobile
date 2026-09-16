import urllib.request
import json 
import pathlib
import datetime

SOUNDBOX_API_FEED = "https://soundbox.blob.core.windows.net/meeting-feeds/feed.json"
HOME_PATH = pathlib.Path.home().joinpath(".clmtimer/")
FEED_PATH =  HOME_PATH.joinpath("meetingfeed.json")

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
    return relevant

if __name__ == "__main__":
    print(get_schedule_data_auto())