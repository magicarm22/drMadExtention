from django.db.models import Q

from mad_extention.models import Items, Inventory, User


def giveItemToUser(userId, itemId, count):
    item = Items.objects.get(id=itemId)
    fragility = getattr(item, 'fragility')
    Inventory.objects.create(userid=User.objects.get(id=userId), itemid=Items.objects.get(id=itemId), count=count,
                             currentfragility=fragility)


def getInventory(userId):
    try:
        inventory = Inventory.objects.select_related('itemid', 'itemid__category').filter(userid=userId)
        print(inventory)
        if inventory is None:
            return []
        else:
            return inventory
    except Exception as e:
        print(e)


def useItem(id, position):
    try:
        inventory = Inventory.objects.filter(id=id).update(inuse=True, position=position)
    except Exception as e:
        print(e)


def isItemOnPosition(userId, position):
    try:
        item = Inventory.objects.filter(Q(userid=userId) & Q(position=position)).first()
        if item is None:
            return False
        return True
    except Exception as e:
        print(e)

def unUseItem(userId, position):
    try:
        item = Inventory.objects.filter(Q(userid=userId) & Q(position=position)).update(inuse=False, position=0)
    except Exception as e:
        print(e)


def getUsableItemsFeatures(userId):
    try:
        items = Inventory.objects.filter(userid=userId).select_related('itemid')\
                        .values_list('itemid__pz', 'itemid__pa', 'itemid__py')
        return items
    except Exception as e:
        print(e)
    return None