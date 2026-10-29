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
    "INTRODUCTION": {
        "id": 0,
        "time": 1
    },
    "TREASURES TALK": {
        "id": 1,
        "time": 10
    },
    "SPIRITUAL GEMS": {
        "id": 2,
        "time": 10
    },
    "BIBLE READING": {
        "id": 3,
        "student": True,
        "time": 4
    },
    "STARTING A CONVERSATION": {
        "id": 4,
        "student": True
    },
    "FOLLOWING UP": {
        "id": 5,
        "student": True
    },
    "WHAT WOULD YOU SAY?": {
        "id": 6,
        "student": False
    },
    "MAKING DISCIPLES": {
        "id": 7,
        "student": True
    },
    "EXPLAINING YOUR BELIEFS": {
        "id": 8,
        "student": True
    },
    "TALK": {
        "id": 9,
        "student": True
    },
    "LIVING TALK": {
        "id": 10
    },
    "CONGREGATION BIBLE STUDY": {
        "id": 11,
        "time": 30
    },
    "CONCLUDING COMMENTS": {
        "id": 12,
        "time": 3
    },
    "PUBLIC TALK": {
        "id": 13,
        "time": 30
    },
    "WATCHTOWER STUDY": {
        "id": 14,
        "time": 60
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
    result = {"apply to ministry": [], "living as christians": []}
    for item in ministry_items:
        talk = {**TALK_TYPES[item[0]], "time": item[1]}
        result["apply to ministry"].append(talk)
    for i, limit in enumerate(living_items):
        talk = {**TALK_TYPES["LIVING TALK"], "time": limit, "talk num": i + 1}
        result["living as christians"].append(talk)
    return result

def get_midweek_schedule(meeting_url_postfix: str):
    result = get_variable_items(meeting_url_postfix)
    result["treasures from gods word"] = [TALK_TYPES["INTRODUCTION"], TALK_TYPES["TREASURES TALK"], TALK_TYPES["SPIRITUAL GEMS"], TALK_TYPES["BIBLE READING"]]
    result["living as christians"] += [TALK_TYPES["CONGREGATION BIBLE STUDY"], TALK_TYPES["CONCLUDING COMMENTS"]]
    return result

def get_weekend_schedule():
    return {"weekend": [TALK_TYPES["PUBLIC TALK"], TALK_TYPES["WATCHTOWER STUDY"]]}

def get_max_schedule():
    result = {}
    links = get_week_schedule_links()
    for year, week in links.keys():
        result[f"{year}-{week}"] = get_midweek_schedule(links[(year, week)])
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
    data = get_max_schedule()
    try:
        with open(CACHE_DIR, "w") as feed:
            json.dump(data, feed, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR]: Something went wrong: {e}")
    return data

def get_schedule_data_auto():
    try:
        with open(CACHE_DIR, "r") as feed:
            data = json.load(feed)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        data = update_schedule_data()
    year, weeknum, dow = datetime.datetime.now().isocalendar()
    if data is None or f"{year}-{weeknum}" not in data:
        data = update_schedule_data()
    return data[f"{year}-{weeknum}"] if dow < 6 else get_weekend_schedule()

def convert(schedule: dict):
    converted = []
    for key in schedule.keys():
        converted += schedule[key]
    return converted