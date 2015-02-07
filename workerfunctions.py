import requests
from redis import Redis


def count_words_at_url(url):
    resp = requests.get(url)
    wordcount = len(resp.text.split())
    redisConnection = Redis()
    redisConnection.set('wordcount', wordcount)


def is_free(userid, location, accelerometer, ringer, call, calendar):
    """
        Input: location (0:home, 1:work, 2:other)
        accelerometer (0:stationary, 1:mobile)
        ringer (0:mute, 1:loud)
        call (1: on call)
        calendar (0:free, 0:busy)
    """
    status = 2

    # Define when free (no acceleration, ringer on, not on call, nothing scheduled)
    if accelerometer == 0 and ringer == 1 and call == 0 and calendar == 0:
        status = 0
    # Define when busy
    if accelerometer == 1 or ringer == 0 or call == 1 or calendar == 1:
        status = 1

    r = Redis()
    r.set(userid, status)
    r.expire(userid, 10)
    return