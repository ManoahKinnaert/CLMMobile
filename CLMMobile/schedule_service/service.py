"""
This service has the goal of figuring out the meeting schedules for this week and upcoming weeks.
"""

from bs4 import BeautifulSoup
import requests 
import datetime 
import pathlib
import json

BASE_URL = "https://wol.jw.org"
URL = f"{BASE_URL}/en/wol/meetings/r1/lp-e"

TALK_TYPES = {
    "STARTING A CONVERSATION": {
        "id": 1,
        "student": True
    },
    "FOLLOWING UP": {
        "id": 2,
        "student": True
    },
    "WHAT WOULD YOU SAY?": {
        "id": 3,
        "student": False
    },
    "MAKING DISCIPLES": {
        "id": 4,
        "student": True
    },
    "EXPLAINING YOUR BELIEFS": {
        "id": 5,
        "student": True
    },
    "TALK": {
        "id": 6,
        "student": True
    }
}

##
##
##  Functions for scraping wol.jw.org to get the meeting schedules.
##
##

def get_content(url: str):
    res = requests.get(url)
    return res.content

def get_week_schedule(year: int, week: int):
    soup = BeautifulSoup(get_content(f"{URL}/{year}/{week}/"), "html.parser")
    link = soup.select_one("a.jwac")["href"]
    obj = soup.find(attrs={"aria-label": "next week"})            
    next_week_data = obj["href"].split("/")[-2:] if obj is not None else None
    return link, next_week_data

def get_week_schedule_links():
    year, week, _ = datetime.datetime.today().isocalendar()
    links = {}
    while True:
        links[(year, week)], next_data = get_week_schedule(year, week)
        if next_data is None: break 
        year, week = map(int, next_data)
    return links 

def get_ministry_items(content: str):
    soup = BeautifulSoup(content, "html.parser")
    links = soup.select("h3.du-fontSize--base.du-color--gold-700.du-margin-top--8.du-margin-bottom--0")
    links = [(int(link["data-pid"]) + 1, link.select_one("strong").get_text(strip=True).split(". ")[1]) for link in links]
    talks = []
    for (pid, name) in links:
        limit = int(soup.find(attrs={"data-pid": pid}).get_text(strip=True).replace("(", "").split(" ")[0])
        talks.append((name.upper(), limit))
    return talks

def get_living_items(content: str):
    soup = BeautifulSoup(content, "html.parser")
    links = [int(link["data-pid"]) + 1 for link in soup.select("h3.du-fontSize--base.du-color--maroon-600.du-margin-top--8.du-margin-bottom--0")] 
    limits = []
    for pid in links[:-1]:
        limit = int(soup.find(attrs={"data-pid": pid}).get_text(strip=True).replace("(", "").split(" ")[0])
        limits.append(limit)
    return limits

def get_variable_items(meeting_url_postfix: str):
    content = get_content(f"{BASE_URL}{meeting_url_postfix}")
    ministry_items = get_ministry_items(content)
    living_items = get_living_items(content)
    return {"apply to ministry": [(TALK_TYPES[item[0]], item[1]) for item in ministry_items], "living as christians": [({"id": 7, "talk num": i + 1}, limit) for i, limit in enumerate(living_items)]}

def get_weekend_schedule():
    return {"weekend": [(TALK_TYPES["PUBLIC TALK"], 30), (TALK_TYPES["WATCHTOWER STUDY"], 60)]}

def get_max_schedule():
    result = {}
    links = get_week_schedule_links()
    for date in links.keys():
        data = get_variable_items(links[date])
        data["treasures"] = [(TALK_TYPES[""], 10), ("")]
        result[date] = get_variable_items(links[date])
    return result

##
##
##  Function for getting the actual result, we choose to cache the result.
##  So we can prevent having to scrape the website every single time.
##
##

HOME_DIR = pathlib.Path.home().joinpath(".clmmobile")
CACHE_DIR = pathlib.Path.home().joinpath("feed/meetingfeed.json")

def update_schedule_data():
    if not CACHE_DIR.parent.exists(): CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(get_max_schedule())
        with open(CACHE_DIR, "w") as feed:
            json.dump(data, feed, ensure_ascii=False, indent=4)
        return data 
    except Exception as e:
        print(f"[ERROR]: Something went wrong: {e}")

def get_schedule_data_auto():
    if not CACHE_DIR.exists(): update_schedule_data()
    try:
        with open(CACHE_DIR, "r") as feed:
            data = json.load(feed)
    except Exception as e:
        pass 
    year, weeknum, dayofweek = datetime.datetime.now().isocalendar()
    if (year, weeknum) not in data:
        data = update_schedule_data()
        # TODO: Add Nonetype check
    if dayofweek < 6:
        schedule = data[(year, weeknum)]
    else:
        pass 