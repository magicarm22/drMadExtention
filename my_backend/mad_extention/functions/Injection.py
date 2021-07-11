import datetime

from django.db.models import F

from functions.Streams import getStreamTime
from mad_extention.models import Injection, User


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
        Injection.objects.filter(userid=userId).update(beforelastinjectiontime=endTime,
                                                       lastinjectiontime=None,
                                                       endinjectiontime=None)
    except Injection.DoesNotExist:
        print("ERROR! Can't stop Injection")


def getCurrentHealth(userId):
    currentTime = datetime.datetime.now().replace(tzinfo=None)
    lastInjectionTime = getInjectionTime(userId)
    beforeLastInjectionTime = getBeforeLastInjectionTime(userId).replace(tzinfo=None)
    endInjectionTime = getEndInjectionTime(userId)
    if lastInjectionTime is None:  # Впервые пришел
        return getHealthInTime(beforeLastInjectionTime.replace(tzinfo=None), currentTime)
    if endInjectionTime is not None and endInjectionTime.replace(tzinfo=None) < currentTime.replace(
            tzinfo=None):  # Укол закончен
        stopInjection(userId, endInjectionTime.replace(tzinfo=None))
        return getHealthInTime(endInjectionTime.replace(tzinfo=None), currentTime)
    hpInInjection = getHealthInTime(beforeLastInjectionTime.replace(tzinfo=None),
                                    lastInjectionTime.replace(tzinfo=None))
    return hpInInjection + (currentTime - lastInjectionTime.replace(tzinfo=None)).total_seconds() / (  # Во время укола
        (endInjectionTime.replace(tzinfo=None) - lastInjectionTime.replace(tzinfo=None)).total_seconds()) * (
                   100 - hpInInjection)


def setZeroHealth(userId, status):
    try:
        user = User.objects.filter(id=userId).update(ishealthzero=status)
        result = True
    except User.DoesNotExist:
        print("ERROR! User didn't find")
        result = False
    return result


def getHealthInTime(startTime, time):
    injectionTime = startTime
    times = getStreamTime(injectionTime, time)
    health = (1 - (times.total_seconds() / (60.0 * 60.0)) / 6) * 100
    if health < 0.0:
        health = 0.0
    # print(health)
    return health


def setInjectionTime(userID, time):
    try:
        inj = Injection.objects.filter(userid=userID).update(lastinjectiontime=time)
        status = True
    except Injection.DoesNotExist:
        print("ERROR! Inj didn't find")
        status = False
    return status


def setEndInjectionTime(userID, time):
    try:
        inj = Injection.objects.filter(userid=userID).update(endinjectiontime=time)
        status = True
    except Injection.DoesNotExist:
        print("ERROR! Inj didn't find")
        status = False
    return status


def increaseInjectionCount(userId):
    try:
        inj = Injection.objects.filter(userid=userId).update(counttimes=F('counttimes') + 1)
        status = True
    except Injection.DoesNotExist:
        print("ERROR! Inj didn't find")
        status = False
    return status


def useInjection(userId, endTime):
    setInjectionTime(userId, datetime.datetime.now())
    setEndInjectionTime(userId, endTime)
    increaseInjectionCount(userId)


def getEndInjectionTimeInMinutes(userId):
    health = getCurrentHealth(userId)
    endTime = getEndInjectionTime(userId)
    if endTime:
        minutes = ((endTime - datetime.datetime.now()).seconds//60)%60 + 1
        print('HERE: ', minutes)
        return minutes
    return 0


def getInjection(userId):
    try:
        health = getCurrentHealth(userId)
        minutes = getEndInjectionTimeInMinutes(userId)
        if minutes:
            return {"status": True, "minutes": minutes}
        if health < 50:
            minutes = int((100 - health) / 4.0) + 1
            useInjection(userId, datetime.datetime.now() + datetime.timedelta(minutes=minutes))
            setZeroHealth(userId, False)
            return {"status": True, "minutes": minutes}
        else:
            return {"status": False, "minutes": 0}
    except Exception as e:
        print(e)
        return {"status": False, "minutes": -1}


