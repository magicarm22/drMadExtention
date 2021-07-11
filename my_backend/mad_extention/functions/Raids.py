import datetime
import random

from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from mad_extention.models import Raids, User, Raidparty


def getListOfRaids():
    try:
        raids = Raidparty.objects.select_related('player1', 'player2', 'player3', 'player4', 'raidid').all()
    except Exception as e:
        print(e)
    return raids


def joinRaid(userId, raidId):
    pass


def isUserInRaidParty(userId):
    try:
        raids = Raidparty.objects.filter(Q(player1__id=userId) | Q(player2__id=userId) |
                                         Q(player3__id=userId) | Q(player4__id=userId)).first()
        if not raids:
            return False
        return True
    except Exception as e:
        print(e)


def getRaidInformationByPartyId(partyId):
    try:
        partyInfo = Raidparty.objects.select_related('raidid').get(id=partyId)
        return partyInfo
    except Exception as e:
        print(e)
    return None


def isRaidStarted(partyId):
    try:
        return Raidparty.objects.get(id=partyId).israidstarted
    except Exception as e:
        print(e)
    return True


def joinRaidParty(partyId, userId):
    try:
        party = Raidparty.objects.get(id=partyId)
        user = User.objects.get(id=userId)
        setattr(party, f'player{party.countplayer + 1}', user)
        setattr(party, 'countplayer', party.countplayer + 1)
        print(party.countplayer)
        party.save()
        pass
    except Exception as e:
        print(e)
