from mad_extention.models import User


def getPills(userId):
    try:
        user = User.objects.get(id=userId)
        res = user.pills
    except User.DoesNotExist:
        print("ERROR! User didn't find")
        res = None
    return res


def setPills(userId, pills):
    try:
        user = User.objects.filter(id=userId).update(pills=pills)
        res = True
    except User.DoesNotExist:
        print("ERROR! User didn't find")
        res = False
    return res
