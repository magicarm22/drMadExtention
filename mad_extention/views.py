import datetime

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


class UserInformation(APIView):

    def get_user(self, name):
        user = User.objects.filter(nickname=name)
        if len(user) == 0:
            return User.objects.create(nickname=name, lastmessage=datetime.datetime.now())
        return user

    def getUsernameById(self, userId):
        headers = {
            'Client-ID': 'j5u27nabr614wgxn8bvsaaz8rpmbwd'
        }
        response = requests.get('https://api.twitch.tv/kraken/users/' + str(userId), headers=headers)
        content = response.content
        print(content)

    def get(self, request, format=None):
        import logging
        logger = logging.getLogger("mylogger")
        logger.info("Whatever to log")
        userId = request.query_params.get('userId', None)
        print(userId)

        # logger.info(request)
        username = self.getUsernameById(userId)
        user = self.get_user(username)
        print(user)
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
        return Response("#123456")


class Utils(APIView):

    def get(self, request):
        userId = request.query_params.get('userId', None)
        clientId = request.query_params.get('userId', None)
        pass

    pass
