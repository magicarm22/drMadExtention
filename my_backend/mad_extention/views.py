import base64
import math

import jwt
from rest_framework import status
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from functions.Injection import getCurrentHealth, getInjection, getEndInjectionTimeInMinutes
from functions.Raids import getListOfRaids, isUserInRaidParty, getRaidInformationByPartyId, isRaidStarted, joinRaidParty
from functions.User import getUser, getUsernameById, calculateUserStats
from mad_extention.conf import settings
from mad_extention.functions.Pills import getPills, setPills
from mad_extention.functions.Shop import getShop, setItemSelled, isItemSelling
from .functions.Inventory import giveItemToUser, getInventory, useItem, isItemOnPosition, unUseItem
from .functions.Items import getItemPrice, getItems


def verifyAndDecode(token):
    try:
        my_secret = base64.b64decode(settings.DRMAD_SECRET)
        print(settings.DRMAD_SECRET, my_secret, token)
        return jwt.decode(token, my_secret, algorithms=['HS256'])
    except Exception as e:
        print(e)
        return None


class UserInformation(APIView):

    def get(self, request, format=None):
        import logging
        # print(request.META.get('HTTP_AUTHORIZATION', ''))
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        print("TOKEN:", token)
        payload = verifyAndDecode(token)
        print(payload)
        logger = logging.getLogger("mylogger")
        logger.info("Whatever to log")
        userId = payload['user_id']
        print(userId)
        token = self.getAuthToken()
        # logger.info(request)
        username = getUsernameById(userId, token)
        user = getUser(userId, username)
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


class Health(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        health = getCurrentHealth(userId)
        return Response({'health': math.ceil(health)})


class StartInjection(APIView):

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        inj = getInjection(userId)
        return Response(inj)

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        minutes = getEndInjectionTimeInMinutes(userId)
        return Response({"errorCode": 0, 'minutes': minutes})


class ShopCenter(APIView):

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        itemId = int(request.data['itemId'])
        if itemId == "":
            return Response({"errorCode": 1, "description": "itemId is None or empty"},
                            status=status.HTTP_404_NOT_FOUND)
        if not isItemSelling(itemId):
            return Response({"errorCode": 2, "description": "This item isn't selling now"},
                            status=status.HTTP_404_NOT_FOUND)
        price = getItemPrice(itemId)
        print(price)
        pills = getPills(userId)
        if pills - price < 0:
            return Response({"errorCode": 3, "description": "You don't have enought money"},
                            status=status.HTTP_404_NOT_FOUND)
        setItemSelled(itemId)
        setPills(userId, pills - price)
        giveItemToUser(userId, itemId, 1)
        return Response({"errorCode": 0, "description": "Success"})

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        verifyAndDecode(token)
        shop = getShop()
        items = getItems(shop[1:6])
        # resultStr = self.formatShopStr(shop[1:6], prices)
        res = {'items': []}
        for item in items:
            if item is None:
                continue
            res['items'].append({
                'itemId': item.id,
                'itemName': item.itemname,
                'mainCategory': item.category.maincategoryname,
                'subCategory': item.category.subcategoryname,
                'pa': item.pa,
                'pz': item.pz,
                'py': item.py,
                'cost': item.cost,
                'fragility': item.fragility
            })

        return Response(res)


class MyInventory(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        inventory = getInventory(userId)
        items = []
        for item in inventory:
            itemJson = {
                'id': item.id,
                'itemId': item.itemid.id,
                'itemName': item.itemid.itemname,
                'count': item.count,
                'fragility': item.currentfragility,
                'mainCategoryName': item.itemid.category.maincategoryname,
                'subCategoryName': item.itemid.category.subcategoryname,
            }
            items.append(itemJson)
        return Response(items)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        id = request.data['id']
        position = request.data['position']
        if isItemOnPosition(userId, position):
            unUseItem(userId, position)
        useItem(id, position)
        return Response({"errorCode": 0, "description": "Success"})


class RaidsInfo(APIView):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        listOfRaids = getListOfRaids()
        result = []
        for raid in listOfRaids:
            print(raid.player1.nickname)
            raidInfo = {
                'raidid': raid.id,
                'countPlayer': raid.countplayer,
                'player1': None if raid.player1 is None else raid.player1.nickname,
                'player2': None if raid.player2 is None else raid.player2.nickname,
                'player3': None if raid.player3 is None else raid.player3.nickname,
                'player4': None if raid.player4 is None else raid.player4.nickname,
                'location': raid.raidid.locationname,
                'isRaidStarted': raid.israidstarted,
            }
            result.append(raidInfo)
        return Response(result)

    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '')[len("Bearer "):]
        payload = verifyAndDecode(token)
        userId = payload['user_id']
        partyId = request.data['partyid']
        if userId == '':
            return Response({"errorCode": 1, "description": "userId is Empty"})
        if isUserInRaidParty(userId):
            return Response({"errorCode": 2, "description": "You are already in party"})
        if isRaidStarted(partyId):
            return Response({"errorCode": 3, "description": "Raid has already started"})
        raidInfo = getRaidInformationByPartyId(partyId)
        print(raidInfo)

        pz, pa, py = calculateUserStats(userId)
        print(pz, pa, py)
        if pa < raidInfo.raidid.pa:
            return Response({"errorCode": 4, "description": "You don't have enough power"})
        # if self.db.getCountCert(userId) != self.db.getTierCert(raidId):
        #     await ctx.send(f"/me {ctx.author.name}, эта локация для вас недоступна")
        #     return
        if getCurrentHealth(userId) < 25:
            return Response({"errorCode": 5, "description": "You have very low health"})
        if raidInfo.countplayer >= 4:
            return Response({"errorCode": 6, "description": "You can't enter to that group, it's full"})
        joinRaidParty(partyId, userId)
        return Response({"errorCode": 0, "description": "Success"})
