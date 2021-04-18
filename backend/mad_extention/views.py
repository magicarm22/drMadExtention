import base64
import datetime
import json

import jwt

import requests
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
import logging, logging.config
import sys

from mad_extention.models import User

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from mad_extention.conf import settings


def verifyAndDecode(token):
    try:
        my_secret = base64.b64decode(settings.DRMAD_SECRET)
        return jwt.decode(token, my_secret, algorithms=['HS256'])
    except Exception as e:
        print(e)
        return None


class UserInformation(APIView):

    def get_user(self, name):
        if name is None:
            return None
        try:
            user = User.objects.get(nickname=name)
        except User.DoesNotExist:
            user = User.objects.create(nickname=name, lastmessage=datetime.datetime.now())
        return user

    def getUsernameById(self, userId, token):
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

    def get(self, request, format=None):
        import logging
        # print(request.META.get('HTTP_AUTHORIZATION', ''))
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        print(payload)
        logger = logging.getLogger("mylogger")
        logger.info("Whatever to log")
        userId = payload['user_id']
        print(userId)
        token = self.getAuthToken()
        # logger.info(request)
        username = self.getUsernameById(userId, token)
        user = self.get_user(username)
        print(user.nickname)
        userInformation = {
            'nickname': str(user.nickname),
            'countRaids': str(user.countraids),
            'countCerts': str(user.countcert),
            'pills': str(user.pills),
            'pa': str(user.pa),
            'pz': str(user.pz),
            'py': str(user.py)
        }
        #     # health = self.getCurrentHealth(userId)
        #     # if health == 0.0 and not self.db.isHealthZero(ctx.author.name):
        #     #     self.db.addEnergy(ctx.author.name, -3)
        #     #     self.db.setZeroHealth(ctx.author.name, True)
        #     # levelInfo = self.db.getCurrentLevel(userId)
        #     # print(levelInfo)
        #     # illnesses = ""
        #     # for level in levelInfo:
        #     #     illnesses += level[0] + ', '
        #     injectionCount = self.db.getInjectionCount(userId)
        #     # info = self.db.getTimeInStream(ctx.author.name)
        #     # if info[0] is None:
        #     #     streamTime = info[1]
        #     # else:
        #     #     streamTime = info[1] + int((datetime.datetime.now() - info[0]).total_seconds() / 60)
        #     # countRaid = self.db.getCountRaids(userId)
        #     # pills = self.getPills(ctx.author.name)
        #     # strStreamTime = self.formatStreamTime(streamTime)
        #     pz, pa, py = self.calculateUserStats(userId)
        #     certs = self.db.getCountCert(userId)
        #     await ctx.send(f'/me Имя: {ctx.author.name} | Класс: {levelInfo[0][1]} '
        #                    f'| Болезни: {illnesses[:-2]} '
        #                    f'| Таблеток: {pills} '
        #                    f'| Количество рейдов: {countRaid} '
        #                    f'| ПЗ: {pz}, ПА: {pa}, ПУ: {py} '
        #                    f'| Количество справок: {certs} '
        #                    f'| Время, проведенное на стриме: {strStreamTime} |')
        return Response(userInformation)

    def getAuthToken(self):
        return "Bearer " + str(settings.DRMAD_OAUTH_TOKEN)


class Utils(APIView):

    def get(self, request):
        userId = request.query_params.get('userId', None)
        clientId = request.query_params.get('userId', None)
        pass

    pass
