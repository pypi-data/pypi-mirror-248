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
    {"name": "di",
     "domain": "di.fm",
     "display_name": "DI.fm",
     "logo_url": "https://cdn.audioaddict.com/di.fm/assets/\
     flux/branding/logo-di@1x-8cf523ebe8d26478fc652ebce3b3a664e7b123b7bddc44297b4fa48d4160b634.png"},
    {"name": "rockradio",
     "domain": "rockradio.com",
     "display_name": "ROCKRADIO.com",
     "logo_url": "https://cdn.audioaddict.com/rockradio.com/assets/\
     logo@1x-59029197dbdd444853cf52fbed9f7a4511740e2b4314ce53937d9c4b8f2c0ced.png"},
    {"name": "radiotunes",
     "domain": "radiotunes.com",
     "display_name": "RadioTunes",
     "logo_url": "https://cdn.audioaddict.com/radiotunes.com/assets/\
     logo-7ecd74b319fa8ca47461e6c5aa8ba3f984983cad5ad16575d29dd3c19d4e5489.svg"},
    {"name": "jazzradio",
     "domain": "jazzradio.com",
     "display_name": "JAZZRADIO.com",
     "logo_url": "https://cdn.audioaddict.com/jazzradio.com/assets/\
     logo-213eba1ee493292d34834889d5d6a87695cb1c06a425aec215d3be9a3b234e46.svg"},
    {"name": "classicalradio",
     "domain": "classicalradio.com",
     "display_name": "ClassicalRadio.com",
     "logo_url": "https://cdn.audioaddict.com/classicalradio.com/assets/\
     logo-1bfff0f5c5b383c0be3f3cb214a7767eac8e3c7114576e15affd9cfaaeba0a72.svg"},
    {"name": "zenradio",
     "domain": "zenradio.com",
     "display_name": "Zen Radio",
     "channel_url_prefix": "zr",
     "logo_url": "https://cdn.audioaddict.com/zenradio.com/assets/\
     logo-339dddf85f742348e460ad3b7812e023c4230b12900c81db319b1525991cb07a.svg"}
]
