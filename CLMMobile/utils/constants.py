import pathlib 

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
STATIC_DIR = ASSETS_DIR / "static"
HOMEPATH = pathlib.Path.home().joinpath(".clmmobile")
SETTINGS_FILE = HOMEPATH.joinpath("settings.json")
TRANS_DIR = ASSETS_DIR / "translations"
MEETING_FEED_CACHE = HOMEPATH.joinpath("feed/meetingfeed.json")

BASE_SCRAPE_URL = "https://wol.jw.org"
MEETING_SCRAPE_URL = f"{BASE_SCRAPE_URL}/en/wol/meetings/r1/lp-e"
