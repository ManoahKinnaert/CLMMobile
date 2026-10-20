"""
This service has the goal of figuring out the meeting schedules for this week and upcoming weeks.
"""

from bs4 import BeautifulSoup
import requests 
import datetime 

BASE_URL = "https://wol.jw.org/en"
URL = f"{BASE_URL}/wol/meetings/r1/lp-e"

def get_week_schedule(year: int, week: int):
    res = requests.get(f"{URL}/{year}/{week}/")
    soup = BeautifulSoup(res.content, "html.parser")
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

def get_field_ministry_items(content):
    pid = 20    # we start with pid 20
     

print(get_week_schedule_links())