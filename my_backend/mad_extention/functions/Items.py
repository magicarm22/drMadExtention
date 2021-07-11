from mad_extention.models import Items, Inventory, User


def getItemPrice(itemId):
    try:
        item = Items.objects.filter(id=itemId).first()
        cost = getattr(item, 'cost')
        return cost
    except:
        pass


def getItems(items):
    itemsInfo = []
    for item in items:
        itemInfo = Items.objects.filter(id=item).select_related('category').first()
        itemsInfo.append(itemInfo)
    return itemsInfo
