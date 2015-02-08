import os
import requests
from redis import Redis
import numpy as np
import pickle
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

def is_free(userid, entry):
    """
    Define user status (0 = free, 1=busy, 2=not sure)

    Input: location (0:home, 1:work, 2:other)
        acceller (0:stationary, 1:mobile)
        silent (0:ringer on, 1:silent/vibrate)
        call (1: on call)
        calendar (0:free, 1:busy)
        chrome (0:productive/other, 1:facebook)
        alarm (time in minutes)
    """
    accelerometer = entry['accelerometer']
    silent = entry['silent']
    on_call = entry['on_call']
    calendar = entry.get('calendar', 0)
    location = entry['location']
    next_alarm = entry['next_alarm']
    chrome = entry.get('chrome', 1)

    # Default to not sure
    status = 2

    # On a call - must be busy
    if on_call == 1:
        status = 1
    # On Facebook - must be free
    elif chrome == 1:
        status = 0
    # At home, not moving, less than 8 hours till next alarm - asleep
    elif location == 0 and next_alarm < 480 and accelerometer == 0:
        status = 1
    # At home, more than 8 hours till next alarm - free
    elif location == 0 and next_alarm > 480:
        status = 0
    # At work in a meeting - busy
    elif location == 1 and calendar == 1:
        status = 1
    # At work phone on silent - busy
    elif location == 1 and silent == 1:
        status = 1
    # Outside, phone on silent - busy
    elif location == 2 and silent == 1:
        status = 1
    # Outside, at an event - busy
    elif location == 2 and calendar == 1:
        status = 1
    # Outside, moving - free
    elif location == 2 and accelerometer == 1:
        status = 0

    r = Redis()
    r.hset(userid, 'status', str(status))
    r.expire(userid, 10)
    return status


def task_duration(userid, rdmforest, entry):
    entry = [entry['accelerometer'], entry['silent'], entry['location']]

    if entry == [0,0,0]:
        output = 451
        return output

    # 12AM
    temp = np.concatenate((np.zeros(8*60),(np.zeros(45)+2))) # sleep + commute
    temp = np.concatenate((temp, np.zeros(4*60+15)+1)) # work
    temp = np.concatenate((temp,np.zeros(60)+2)) # lunch
    temp = np.concatenate((temp,np.zeros(4*60)+1)) # work
    temp = np.concatenate((temp,np.zeros(45)+2))  # commute
    location = np.concatenate((temp,np.zeros(5*60+15)))  # sleep

    #calendar = [np.zeros(10*60),np.zeros(45)+1,np.zeros(13*60)+15]
    temp = np.concatenate((np.zeros(8*60),np.zeros(45)+1)) # sleep + commute
    temp = np.concatenate((temp,np.zeros(4*60+15)))  # work
    temp = np.concatenate((temp,np.zeros(60))) # lunch
    temp = np.concatenate((temp,np.zeros(4*60))) # work
    temp = np.concatenate((temp,np.zeros(45)+1)) # commute
    acceller = np.concatenate((temp,np.zeros(5*60+15))) # home
    #acceller = [np.zeros(8*60),np.zeros(45)+1,np.zeros(4*60+15),np.zeros(60),np.zeros(4*60),np.zeros(45)+1,np.zeros(5*60+15)]

    temp = np.concatenate((np.zeros(10*60+15),np.zeros(7*60+45)+1))
    ringer = np.concatenate((temp,np.zeros(6*60)))

    # Features
    X = np.array([acceller.tolist(),ringer.tolist(),location.tolist()]).T

    # Labels
    lengths = np.zeros(1440)+1
    for i in range(0,X.shape[0]-1):
        length = 1
        for j in range(i+1,X.shape[0]):
            if np.any(X[i,:]!=X[j,:]):
                lengths[i] = length
                break
            else:
                length += 1

    enc = preprocessing.OneHotEncoder()
    enc.fit(X)

    # Transform input from categorical to continuous
    myinput = enc.transform(X).toarray()

    # rdmforest = RandomForestClassifier()
    rdmforest.fit(myinput, lengths)

    output = rdmforest.predict(enc.transform([entry]).toarray())[0]

    r = Redis()
    r.hset(userid, 'status_time', int(output))
    r.expire(userid, 10)
    return output


def update_status(userid):
    # Load model
    _basedir = os.path.abspath(os.path.dirname(__file__))
    modelFile = os.path.join(_basedir, 'randomForestModel')
    model = pickle.load(open(modelFile,'rb'))

    # Load user attributes
    r = Redis()
    keyValuePairs = r.hgetall(userid)
    keyValuePairs['location'] = 1 # At work, mocked TODO: Get real value
    # entry = [keyValuePairs['accelerometer'], keyValuePairs['silent'], keyValuePairs['location']]

    status_duration = task_duration(userid, model, keyValuePairs)
    status = is_free(userid, keyValuePairs)

    return (status_duration, status)


