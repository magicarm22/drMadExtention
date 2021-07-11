from django.db.models import Q

from mad_extention.models import Streams


def getStreamTime(fromTime, toTime):
    streams = getStreamTimeFrom(fromTime)
    print(streams.first().__dict__)
    if fromTime.replace(tzinfo=None) < streams.first().startedat.replace(tzinfo=None):
        startTime = streams.first().endedat
    else:
        startTime = fromTime
    if streams.first().endedat is None:
        times = toTime.replace(tzinfo=None) - startTime.replace(tzinfo=None)
    else:
        times = streams.first().endedat.replace(tzinfo=None) - startTime.replace(tzinfo=None)
        # print(times)
        for stream in streams[1:]:
            if stream.endedat is None:
                times += toTime.replace(tzinfo=None) - stream.startedat.replace(tzinfo=None)
            else:
                times += stream.endedat.replace(tzinfo=None) - stream.startedat.replace(tzinfo=None)
    print(times)
    return times


def getStreamTimeFrom(fromTime):
    print(fromTime)
    try:
        streams = Streams.objects.filter(Q(endedat__gt=fromTime) | Q(endedat=None)).order_by('startedat')
    except Streams.DoesNotExist:
        print("ERROR! User didn't find")
        streams = None
    return streams
