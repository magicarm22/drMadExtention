import json

import requests
from django.apps import AppConfig
from mad_extention.conf import settings


class MadExtentionConfig(AppConfig):
    name = 'mad_extention'

    def ready(self):
        params = {
            "client_id": settings.DRMAD_CLIENT_ID,
            "client_secret": settings.DRMAD_TWITCH_API_SECRET,
            "grant_type": "client_credentials"
        }
        r = requests.post("https://id.twitch.tv/oauth2/token", params=params)
        settings.DRMAD_OAUTH_TOKEN = json.loads(r.text)['access_token']
        print(settings.DRMAD_OAUTH_TOKEN)