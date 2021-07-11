import datetime
import random

from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver

from mad_extention.models import Shop, Items


def deleteShop():
    try:
        Shop.objects.get().delete()
        return None
    except Shop.DoesNotExist:
        return None


def getAllItems():
    try:
        items = Items.objects.all()
    except:
        items = None
    return items


def addShop(shopItems):
    try:
        items = []
        for i in range(0, 5):
            items.append(Items.objects.filter(id=shopItems[i]).first())
        items = Shop.objects.create(lastchanges=datetime.datetime.now(),
                                    currentitem1=items[0], currentitem2=items[1],
                                    currentitem3=items[2], currentitem4=items[3],
                                    currentitem5=items[4])
    except Exception as e:
        print("Магазин не создан! {}".format(e))
        items = None
    return items


def createShop():
    items = getAllItems()
    itemsId = []
    itemsChance = []
    for item in items:
        itemsId.append(item.id)
        itemsChance.append(item.shopchance)
    # for i in range(0, 20):
    shopItems = random.choices(itemsId, itemsChance, k=5)
    # if not self.db.shopExist():
    addShop(shopItems)
    return getShop()


def getShop():
    try:
        shop = Shop.objects.values_list('lastchanges', 'currentitem1', 'currentitem2',
                                        'currentitem3', 'currentitem4', 'currentitem5').first()
        if shop is None:
            shop = createShop()
    except Shop.DoesNotExist:
        shop = createShop()
    return shop


def setItemSelled(itemId):
    try:
        shop = Shop.objects.values_list('currentitem1', 'currentitem2',
                                        'currentitem3', 'currentitem4', 'currentitem5')
        print(shop)
        for i in range(1, len(shop[0]) + 1):
            print(shop[0][i - 1], itemId)
            if shop[0][i - 1] == itemId:
                kwargs = {
                    f"currentitem{i}": None
                }
                break
        Shop.objects.update(**kwargs)
    except Exception as e:
        print(f"Item didn't find: {e}")
        pass


def isItemSelling(itemId):
    try:
        shop = Shop.objects.filter(Q(currentitem1=itemId) | Q(currentitem2=itemId) | Q(currentitem3=itemId) |
                                   Q(currentitem4=itemId) | Q(currentitem5=itemId))
        if shop is not None:
            return True
        return False
    except:
        return False
