import datetime
import json
import time
from threading import Thread

import requests
from django.apps import AppConfig

from mad_extention.conf import settings


class MadExtentionConfig(AppConfig):
    name = 'mad_extention'

    def getStreamStatus(self):
        while True:
            headers = {
                'Authorization': self.getAuthToken(),
                "Client-Id": settings.DRMAD_CLIENT_ID
            }
            params = {
                "user_id": str(settings.DRMAD_USER_ID)
            }
            r = requests.get("https://api.twitch.tv/helix/streams",
                             headers=headers, params=params)
            data_json = json.loads(r.text)
            if len(data_json['data']) != 0:
                settings.DRMAD_STREAM_STATUS = True
            else:
                settings.DRMAD_STREAM_STATUS = False
            print(settings.DRMAD_STREAM_STATUS)
            time.sleep(30)

    def ready(self):
        params = {
            "client_id": settings.DRMAD_CLIENT_ID,
            "client_secret": settings.DRMAD_TWITCH_API_SECRET,
            "grant_type": "client_credentials"
        }
        r = requests.post("https://id.twitch.tv/oauth2/token", params=params)
        settings.DRMAD_OAUTH_TOKEN = json.loads(r.text)['access_token']
        print(settings.DRMAD_OAUTH_TOKEN)

        self.bots = self.getBots()
        t = Thread(target=self.getStreamStatus)
        t.start()
        t = Thread(target=self.userTime)
        t.start()


    def getAuthToken(self):
        return "Bearer " + str(settings.DRMAD_OAUTH_TOKEN)

    def userTime(self):
        while True:
            if not settings.DRMAD_STREAM_STATUS:
                try:
                    r = requests.get(f"http://tmi.twitch.tv/group/user/{settings.DRMAD_CHANNEL_NAME}/chatters")
                    res = json.loads(r.text)
                    chatters = res['chatters']
                    allViewers = chatters['vips'] + chatters['moderators'] + chatters['viewers'] + chatters[
                        'broadcaster']
                    print(allViewers)
                    for person in allViewers:
                        if person not in self.bots:
                            if not self.isUserNew(person):
                                timeIn = self.getLastTimeIn(person)
                                if timeIn is None:
                                    self.setLastTimeIn(person, datetime.datetime.now())
                    print("HERE")
                    if self.isTimeChangeShop(15):
                        print("CHANGE")
                        self.changeShop()
    #                 leftUsers = self.db.getAllLeftPersons(allViewers)
    #                 for user in leftUsers:
    #                     nickname = user[0]
    #                     self.calcTimeCount(nickname)
    #                     self.calcPills(nickname)
    #                     self.db.setLastTimeIn(nickname, None)
                except Exception as e:
                    print(e)
                    pass
                # silenceUsers = self.db.getSilenceUsers(20)
    #             for user in silenceUsers:
    #                 self.db.addEnergy(user, -1)
    #                 self.db.setLastMessage(user, datetime.datetime.now())
    #             self.db.deleteOldTrades(10)
    #
    #             lastRaidsTime = self.db.getLastRaidsTime()
    #             if lastRaidsTime is None:
    #                 self.db.createRaidTime()
    #             else:
    #                 streamTime = self.getStreamTime(lastRaidsTime, datetime.datetime.now()).total_seconds()
    #                 if self.db.isRaidTime():
    #                     if streamTime / 60 >= 30:
    #                         self.db.setRaidsTime(False)
    #                         self.db.deleteNotReadyParties()
    #                         await ws.send_privmsg(os.environ['CHANNEL'], "/me Наступило утро, и снова началась "
    #                                                                      "размеренная жизнь. Команда !raid заблокированна, "
    #                                                                      "все не отправленные группы расформированны.")
    #                 else:
    #                     if streamTime / 60 >= 60:
    #                         self.db.setRaidsTime(True)
    #                         await ws.send_privmsg(os.environ['CHANNEL'], "/me Наступила ночь! "
    #                                                                      "Самое время немного подебоширить! "
    #                                                                      "Используй команду !raid, чтобы начать")
            time.sleep(60)

    def getBots(self):
        from mad_extention.models import Bots

        bots = [x[0] for x in list(Bots.objects.all().values_list('botname'))]
        print(bots)
        return bots

    def isUserNew(self, person):
        from mad_extention.models import User
        try:
            user = User.objects.get(nickname=person)
            return False
        except User.DoesNotExist:
            return True
        pass

    def getLastTimeIn(self, person):
        from mad_extention.models import User
        try:
            user = User.objects.get(nickname=person).values_list('lasttimein')
            return user[0]
        except User.DoesNotExist:
            return None
        pass

    def setLastTimeIn(self, person, time):
        from mad_extention.models import User
        try:
            user = User.objects.filter(nickname=person).update(lasttimein=time)
            return True
        except User.DoesNotExist:
            return False
        pass

    def isTimeChangeShop(self, minutes):
        from mad_extention.models import Shop
        try:
            shop = Shop.objects.filter(lastchanges__lt=(datetime.datetime.now() - datetime.timedelta(minutes=minutes)))
            print(shop)
            if len(shop) == 0:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            return False
        pass

    def changeShop(self):
        from functions.Shop import createShop, deleteShop
        # print("BBBB")
        # print("Changing Shop")
        deleteShop()
        createShop()
        pass
