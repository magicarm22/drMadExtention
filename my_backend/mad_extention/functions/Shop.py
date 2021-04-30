import datetime
import random

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
        if len(shop) == 0:
            shop = createShop()
    except Shop.DoesNotExist:
        shop = createShop()
    return shop
