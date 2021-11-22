from django.shortcuts import render

# Create your views here.
def time_normalization(time):
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour if int(time.hour)>10 else '0'+ str(time.hour)
    minute = time.minute if int(time.minute)>10 else '0'+ str(time.minute)
    second = time.second if int(time.second)>10 else '0'+ str(time.second)
    return {
        "year":year,
        "month":month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
    }
