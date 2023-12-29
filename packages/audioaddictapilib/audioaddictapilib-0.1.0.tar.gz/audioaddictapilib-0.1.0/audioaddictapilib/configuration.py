from random import choice

API_BASE_URL = "https://api.audioaddict.com/v1"
VALID_SERVERS = ['prem1', 'prem2', 'prem4']
LISTEN_BASE_URL = f"http://{choice(VALID_SERVERS)}.{{domain}}"

LOGO_TYPES = [
    "horizontal_banner",
    "tall_banner",
    "vertical",
    "default",
    "square",
    "compact"
]

SERVICES = [
    {"name": "di", "domain": "di.fm"},
    {"name": "rockradio", "domain": "rockradio.com"},
    {"name": "radiotunes", "domain": "radiotunes.com"},
    {"name": "jazzradio", "domain": "jazzradio.com"},
    {"name": "classicalradio", "domain": "classicalradio.com"},
    {"name": "zenradio", "domain": "zenradio.com", "channel_url_prefix": "zr"}
]
