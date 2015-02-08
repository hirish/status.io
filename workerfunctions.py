import os
import requests
from redis import Redis
import numpy as np
import pickle
# from sklearn import preprocessing
# from sklearn.ensemble import RandomForestClassifier

def is_free(userid, entry):
    """
        Input: entry contains
        location (0:home, 1:work, 2:other)
        accelerometer (0:stationary, 1:mobile)
        ringer (0:mute, 1:loud)
        call (1: on call)
        calendar (0:free, 0:busy)
    """
    accelerometer = entry['accelerometer']
    silent = entry['silent']
    on_call = entry['on_call']
    calendar = 0

    status = 2

    # Define when free (no acceleration, ringer on, not on call, nothing scheduled)
    if accelerometer == 0 and silent == 0 and on_call == 0 and calendar == 0:
        status = 0
    # Define when busy
    if accelerometer == 1 or silent == 1 or on_call == 1 or calendar == 1:
        status = 1

    r = Redis()
    r.hset(userid, 'status', status)
    r.expire(userid, 10)
    return status


def task_duration(rdmforest, entry):
    """
    Predict current task duration given:
    entry = [accel,ringer,loc]
    - acceleration (0: stationary, 1:mobile)
    - silent (0: loud, 1: silent)
    - location (0:home, 1:work, 2:other)
    """
    #TODO Remove
    return 0

    # entry = [entry['accelerometer'], entry['silent'], entry['location']]
    #
    # if entry == [0,0,0]:
    #     output = 451
    #     return output
    #
    # # 12AM
    # temp = np.concatenate((np.zeros(8*60),(np.zeros(45)+2))) # sleep + commute
    # temp = np.concatenate((temp, np.zeros(4*60+15)+1)) # work
    # temp = np.concatenate((temp,np.zeros(60)+2)) # lunch
    # temp = np.concatenate((temp,np.zeros(4*60)+1)) # work
    # temp = np.concatenate((temp,np.zeros(45)+2))  # commute
    # location = np.concatenate((temp,np.zeros(5*60+15)))  # sleep
    #
    # #calendar = [np.zeros(10*60),np.zeros(45)+1,np.zeros(13*60)+15]
    # temp = np.concatenate((np.zeros(8*60),np.zeros(45)+1)) # sleep + commute
    # temp = np.concatenate((temp,np.zeros(4*60+15)))  # work
    # temp = np.concatenate((temp,np.zeros(60))) # lunch
    # temp = np.concatenate((temp,np.zeros(4*60))) # work
    # temp = np.concatenate((temp,np.zeros(45)+1)) # commute
    # acceller = np.concatenate((temp,np.zeros(5*60+15))) # home
    # #acceller = [np.zeros(8*60),np.zeros(45)+1,np.zeros(4*60+15),np.zeros(60),np.zeros(4*60),np.zeros(45)+1,np.zeros(5*60+15)]
    #
    # temp = np.concatenate((np.zeros(10*60+15),np.zeros(7*60+45)+1))
    # ringer = np.concatenate((temp,np.zeros(6*60)))
    #
    # # Features
    # X = np.array([acceller.tolist(),ringer.tolist(),location.tolist()]).T
    #
    # # Labels
    # lengths = np.zeros(1440)+1
    # for i in range(0,X.shape[0]-1):
    #     length = 1
    #     for j in range(i+1,X.shape[0]):
    #         if np.any(X[i,:]!=X[j,:]):
    #             lengths[i] = length
    #             break
    #         else:
    #             length += 1
    #
    # enc = preprocessing.OneHotEncoder()
    # enc.fit(X)
    #
    # # Transform input from categorical to continuous
    # myinput = enc.transform(X).toarray()
    #
    # rdmforest = RandomForestClassifier()
    # rdmforest.fit(myinput, lengths)
    #
    # output = rdmforest.predict(enc.transform([entry]).toarray())[0]
    #
    # return output


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

    status_duration = task_duration(model, keyValuePairs)
    status = is_free(userid)


