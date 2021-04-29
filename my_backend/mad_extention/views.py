import base64
import datetime
import json
import math

import jwt

import requests
from django.db.models import Q, F
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
import logging, logging.config
import sys

from mad_extention.models import User, Injection, Streams

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

    def getUser(self, userId, name):
        if name is None:
            return None
        try:
            user = User.objects.get(id=userId, nickname=name)
        except User.DoesNotExist:
            user = User.objects.create(id=userId,nickname=name, lastmessage=datetime.datetime.now())
            user.save()
            inj = Injection.objects.create(userid=user, beforelastinjectiontime=datetime.datetime.now())
            inj.save()
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
        user = self.getUser(userId, username)
        print(user.nickname)
        userInformation = {
            'nickname': str(user.nickname),
            'countRaids': str(user.countraids),
            'countCerts': str(user.countcert),
            'pills': str(int(user.pills)),
            'pa': str(user.pa),
            'pz': str(user.pz),
            'py': str(user.py)
        }
        print(userInformation)
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


def getInjectionTime(userId):
    try:
        inj = Injection.objects.get(userid=userId)
    except Injection.DoesNotExist:
        print("ERROR! User didn't find")
        inj = None
    return inj.lastinjectiontime


def getBeforeLastInjectionTime(userId):
    try:
        inj = Injection.objects.get(userid=userId)
    except Injection.DoesNotExist:
        print("ERROR! User didn't find")
        inj = None
    return inj.beforelastinjectiontime


def getEndInjectionTime(userId):
    try:
        inj = Injection.objects.get(userid=userId)
    except Injection.DoesNotExist:
        print("ERROR! User didn't find")
        inj = None
    return inj.endinjectiontime


def stopInjection(userId, endTime):
    try:
        Injection.objects.filter(userid=userId).update(beforeLastInjectionTime=endTime,
                                                         lastInjectionTime=None,
                                                         endInjectionTime=None)
    except User.DoesNotExist:
        print("ERROR! Can't stop Injection")


def getStreamTimeFrom(fromTime):
    print(fromTime)
    try:
        streams = Streams.objects.filter(Q(endedat__gt=fromTime) | Q(endedat=None)).order_by('startedat')
    except User.DoesNotExist:
        print("ERROR! User didn't find")
        streams = None
    return streams


def getStreamTime(fromTime, toTime):
    streams = getStreamTimeFrom(fromTime)
    print(streams.first().__dict__)
    if fromTime.replace(tzinfo=None) < streams.first().startedat.replace(tzinfo=None):
        startTime = streams.first().endedat
    else:
        startTime = fromTime
    if streams.first().endedat is None:
        times = toTime.replace(tzinfo=None) - startTime.replace(tzinfo=None)
    else:
        times = streams.first().endedat.replace(tzinfo=None) - startTime.replace(tzinfo=None)
        # print(times)
        for stream in streams[1:]:
            if stream.endedat is None:
                times += toTime.replace(tzinfo=None) - stream.startedat.replace(tzinfo=None)
            else:
                times += stream.endedat.replace(tzinfo=None) - stream.startedat.replace(tzinfo=None)
    print(times)
    return times


def getHealthInTime(startTime, time):
    injectionTime = startTime
    times = getStreamTime(injectionTime, time)
    health = (1 - (times.total_seconds() / (60.0 * 60.0)) / 6) * 100
    if health < 0.0:
        health = 0.0
    # print(health)
    return health


def getCurrentHealth(userId):
    currentTime = datetime.datetime.now().replace(tzinfo=None)
    lastInjectionTime = getInjectionTime(userId).replace(tzinfo=None)
    beforeLastInjectionTime = getBeforeLastInjectionTime(userId).replace(tzinfo=None)
    endInjectionTime = getEndInjectionTime(userId).replace(tzinfo=None)
    if lastInjectionTime is None:  # Впервые пришел
        return getHealthInTime(beforeLastInjectionTime, currentTime)
    if endInjectionTime is not None and endInjectionTime < currentTime:  # Укол закончен
        stopInjection(userId, endInjectionTime)
        return getHealthInTime(endInjectionTime, currentTime)
    hpInInjection = getHealthInTime(beforeLastInjectionTime, lastInjectionTime)
    return hpInInjection + (currentTime - lastInjectionTime).total_seconds() / (  # Во время укола
        (endInjectionTime - lastInjectionTime).total_seconds()) * (100 - hpInInjection)


def setZeroHealth(userId, status):
    try:
        user = User.objects.get(id=userId).update(ishealthzero=status)
        result = True
    except User.DoesNotExist:
        print("ERROR! User didn't find")
        result = False
    return result


class Health(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        health = getCurrentHealth(userId)
        return Response({'health': math.ceil(health)})

class StartInjection(APIView):

    @staticmethod
    def setInjectionTime(userID, time):
        try:
            inj = Injection.objects.filter(userid=userID).update(lastinjectiontime=time)
            status = True
        except User.DoesNotExist:
            print("ERROR! Inj didn't find")
            status = False
        return status

    @staticmethod
    def setEndInjectionTime(userID, time):
        try:
            inj = Injection.objects.filter(userid=userID).update(endinjectiontime=time)
            status = True
        except User.DoesNotExist:
            print("ERROR! Inj didn't find")
            status = False
        return status

    def increaseInjectionCount(self, userId):
        try:
            inj = Injection.objects.filter(userid=userId).update(counttimes=F('counttimes') + 1)
            status = True
        except User.DoesNotExist:
            print("ERROR! Inj didn't find")
            status = False
        return status

    def useInjection(self, userId, endTime):
        self.setInjectionTime(userId, datetime.datetime.now())
        self.setEndInjectionTime(userId, endTime)
        self.increaseInjectionCount(userId)

    def getInjection(self, userId):
        try:
            health = getCurrentHealth(userId)
            if getEndInjectionTime(userId):
                minutes = int((100 - health) / 4.0) + 1
                return {"status": True, "minutes": minutes}
            if health < 50:
                minutes = int((100 - health) / 4.0) + 1
                self.useInjection(userId, datetime.datetime.now() + datetime.timedelta(minutes=minutes))
                setZeroHealth(userId, False)
                return {"status": True, "minutes": minutes}
            else:
                return {"status": False, "minutes": 0}
        except Exception as e:
            print(e)
            return {"status": False, "minutes": -1}

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        inj = self.getInjection(userId)
        return Response(inj)
