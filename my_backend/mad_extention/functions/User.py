import datetime
import json

import requests

from functions.Inventory import getUsableItemsFeatures
from mad_extention.conf import settings

from mad_extention.models import User, Injection


def getUser(userId, name=''):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        user = User.objects.create(id=userId, nickname=name, lastmessage=datetime.datetime.now())
        user.save()
        inj = Injection.objects.create(userid=user, beforelastinjectiontime=datetime.datetime.now())
        inj.save()
    return user


def getUsernameById(userId, token):
    headers = {
        'Authorization': token,
        "Client-Id": settings.DRMAD_CLIENT_ID
    }
    params = {
        "id": str(userId)
    }
    response = requests.get('https://api.twitch.tv/helix/users', params=params, headers=headers)
    content = json.loads(response.content)
    print(content)
    return content['data'][0]['login']


def calculateUserStats(userId):
    userInfo = getUser(userId)
    features = getUsableItemsFeatures(userId)
    indexes = [userInfo.pz, userInfo.pa, userInfo.py]
    print("ind:", indexes)
    pz = indexes[0]
    pa = indexes[1]
    py = indexes[2]
    print(features)
    for feat in features:
        pz += feat[0]
        pa += feat[1]
        py += feat[2]
    return pz, pa, py
