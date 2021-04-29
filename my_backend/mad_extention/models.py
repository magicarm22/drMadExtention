# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid

from django.db import models


class Bots(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    botname = models.TextField(db_column='botName')  # Field name made lowercase.

    class Meta:
        db_table = 'Bots'


class Categoryitem(models.Model):
    maincategoryname = models.TextField(db_column='mainCategoryName')  # Field name made lowercase.
    subcategoryname = models.TextField(db_column='subCategoryName', blank=True, null=True)  # Field name made lowercase.
    itemscanbeused = models.IntegerField(db_column='itemsCanBeUsed', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'CategoryItem'


class Feedbacks(models.Model):
    feedback = models.TextField(blank=True, null=True)
    author = models.ForeignKey('User', models.DO_NOTHING, db_column='author', blank=True, null=True)
    timecreated = models.DateTimeField(db_column='timeCreated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Feedbacks'


class Injection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    lastinjectiontime = models.DateTimeField(db_column='lastInjectionTime', blank=True, null=True)  # Field name made lowercase.
    counttimes = models.IntegerField(db_column='countTimes', blank=True, null=True)  # Field name made lowercase.
    endinjectiontime = models.DateTimeField(db_column='endInjectionTime', blank=True, null=True)  # Field name made lowercase.
    beforelastinjectiontime = models.DateTimeField(db_column='beforeLastInjectionTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Injection'


class Inventory(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    itemid = models.ForeignKey('Items', models.DO_NOTHING, db_column='itemId')  # Field name made lowercase.
    count = models.IntegerField()
    inuse = models.BooleanField(db_column='inUse')  # Field name made lowercase.
    currentfragility = models.IntegerField(db_column='currentFragility', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Inventory'


class Items(models.Model):
    itemname = models.TextField(db_column='itemName')  # Field name made lowercase.
    category = models.ForeignKey(Categoryitem, models.DO_NOTHING)
    pz = models.IntegerField()
    pa = models.IntegerField()
    py = models.IntegerField()
    cost = models.IntegerField(blank=True, null=True)
    shopchance = models.FloatField(db_column='shopChance', blank=True, null=True)  # Field name made lowercase.
    fragility = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Items'


class Levels(models.Model):
    levelname = models.TextField(db_column='levelName')  # Field name made lowercase.
    minenergy = models.IntegerField(db_column='minEnergy')  # Field name made lowercase.
    maxenergy = models.IntegerField(db_column='maxEnergy')  # Field name made lowercase.
    class_field = models.TextField(db_column='class', blank=True, null=True)  # Field renamed because it was a Python reserved word.

    class Meta:
        db_table = 'Levels'


class Raidparty(models.Model):
    player1 = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='player1', blank=True, null=True)
    player2 = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='player2', blank=True, null=True)
    player3 = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='player3', blank=True, null=True)
    player4 = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='player4', blank=True, null=True)
    countplayer = models.IntegerField(db_column='countPlayer', blank=True, null=True)  # Field name made lowercase.
    partycreated = models.DateTimeField(db_column='partyCreated', blank=True, null=True)  # Field name made lowercase.
    raidid = models.ForeignKey('Raids', models.DO_NOTHING, db_column='raidId', blank=True, null=True)  # Field name made lowercase.
    israidstarted = models.BooleanField(db_column='isRaidStarted')  # Field name made lowercase.
    raidended = models.DateTimeField(db_column='raidEnded', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'RaidParty'


class Raidtime(models.Model):
    lastraidstime = models.DateTimeField(db_column='lastRaidsTime')  # Field name made lowercase.
    israidtime = models.BooleanField(db_column='isRaidTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'RaidTime'


class Raids(models.Model):
    locationname = models.TextField(db_column='locationName')  # Field name made lowercase.
    pz = models.IntegerField()
    pa = models.IntegerField()
    loot = models.TextField(blank=True, null=True)  # This field type is a guess.
    time = models.IntegerField()
    minuserpa = models.IntegerField(db_column='minUserPA', blank=True, null=True)  # Field name made lowercase.
    minpills = models.IntegerField(db_column='minPills', blank=True, null=True)  # Field name made lowercase.
    maxpills = models.IntegerField(db_column='maxPills', blank=True, null=True)  # Field name made lowercase.
    tiercert = models.IntegerField(db_column='tierCert', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Raids'


class Shop(models.Model):
    lastchanges = models.DateTimeField(db_column='lastChanges')  # Field name made lowercase.
    currentitem1 = models.ForeignKey(Items, models.DO_NOTHING, db_column='currentItem1', related_name='+', blank=True, null=True)  # Field name made lowercase.
    currentitem2 = models.ForeignKey(Items, models.DO_NOTHING, db_column='currentItem2', related_name='+', blank=True, null=True)  # Field name made lowercase.
    currentitem3 = models.ForeignKey(Items, models.DO_NOTHING, db_column='currentItem3', related_name='+', blank=True, null=True)  # Field name made lowercase.
    currentitem4 = models.ForeignKey(Items, models.DO_NOTHING, db_column='currentItem4', related_name='+', blank=True, null=True)  # Field name made lowercase.
    currentitem5 = models.ForeignKey(Items, models.DO_NOTHING, db_column='currentItem5', related_name='+', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Shop'


class Streams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    streamname = models.TextField(db_column='streamName', blank=True, null=True)  # Field name made lowercase.
    startedat = models.DateTimeField(db_column='startedAt', blank=True, null=True)  # Field name made lowercase.
    endedat = models.DateTimeField(db_column='endedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Streams'


class Trade(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    fromuser = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='fromUser')  # Field name made lowercase.
    touser = models.ForeignKey('User', models.DO_NOTHING, related_name='+', db_column='toUser')  # Field name made lowercase.
    item = models.ForeignKey(Items, models.DO_NOTHING, db_column='item')
    price = models.IntegerField()
    tradetime = models.DateTimeField(db_column='tradeTime')  # Field name made lowercase.

    class Meta:
        db_table = 'Trade'


class User(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField(primary_key=True, editable=False)
    nickname = models.TextField(unique=True, blank=True, null=True)
    lastmessage = models.DateTimeField(db_column='lastMessage', blank=True, null=True)  # Field name made lowercase.
    lasttimein = models.DateTimeField(db_column='lastTimeIn', blank=True, null=True)  # Field name made lowercase.
    timecount = models.IntegerField(db_column='timeCount', blank=True, null=True, default=0)  # Field name made lowercase.
    pills = models.FloatField(blank=True, null=True, default=15)
    messagescount = models.IntegerField(db_column='messagesCount', default=0)  # Field name made lowercase.
    energy = models.IntegerField(default=0)
    ishealthzero = models.BooleanField(db_column='isHealthZero', blank=True, null=True, default=False)  # Field name made lowercase.
    countraids = models.IntegerField(db_column='countRaids', blank=True, null=True,default=0)  # Field name made lowercase.
    countcert = models.IntegerField(db_column='countCert', blank=True, null=True, default=0)  # Field name made lowercase.
    pz = models.IntegerField(blank=True, null=True, default=0)
    pa = models.IntegerField(blank=True, null=True, default=0)
    py = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'User'
