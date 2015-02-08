from flask import Flask
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing

from models import db

import os
import api
import main

app = Flask(__name__)

_basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(_basedir, 'app_dev.db')

db.init_app(app)

app.register_blueprint(api.blueprint)
app.register_blueprint(main.blueprint)

#
# def train_model():
#     # Generate synthetic training data
#     temp = np.concatenate((np.zeros(8*60),(np.zeros(45)+2))) # sleep + commute
#     temp = np.concatenate((temp, np.zeros(4*60+15)+1)) # work
#     temp = np.concatenate((temp,np.zeros(60)+2)) # lunch
#     temp = np.concatenate((temp,np.zeros(4*60)+1)) # work
#     temp = np.concatenate((temp,np.zeros(45)+2))  # commute
#     location = np.concatenate((temp,np.zeros(5*60+15)))  # sleep
#
#     #calendar = [np.zeros(10*60),np.zeros(45)+1,np.zeros(13*60)+15]
#     temp = np.concatenate((np.zeros(8*60),np.zeros(45)+1)) # sleep + commute
#     temp = np.concatenate((temp,np.zeros(4*60+15)))  # work
#     temp = np.concatenate((temp,np.zeros(60))) # lunch
#     temp = np.concatenate((temp,np.zeros(4*60))) # work
#     temp = np.concatenate((temp,np.zeros(45)+1)) # commute
#     acceller = np.concatenate((temp,np.zeros(5*60+15))) # home
#     #acceller = [np.zeros(8*60),np.zeros(45)+1,np.zeros(4*60+15),np.zeros(60),np.zeros(4*60),np.zeros(45)+1,np.zeros(5*60+15)]
#
#     temp = np.concatenate((np.zeros(10*60+15),np.zeros(7*60+45)+1))
#     ringer = np.concatenate((temp,np.zeros(6*60)))
#
#     # Features
#     X = np.array([acceller.tolist(),ringer.tolist(),location.tolist()]).T
#
#     # Labels
#     lengths = np.zeros(1440)+1
#     for i in range(0,X.shape[0]-1):
#         length = 1
#         for j in range(i+1,X.shape[0]):
#             if np.any(X[i,:]!=X[j,:]):
#                 lengths[i] = length
#                 break
#             else:
#                 length += 1
#
#
#     enc = preprocessing.OneHotEncoder()
#     enc.fit(X)
#
#     # Transform input from categorical to continuous
#     myinput = enc.transform(X).toarray()
#
#     # Train random forest
#
#     rdmforest = RandomForestClassifier()
#     rdmforest.fit(myinput, lengths)
#
#     return rdmforest

# randomForest = train_model()
randomForest = 'TODO'
modelFile = os.path.join(_basedir, 'randomForestModel')
pickle.dump(randomForest, open(modelFile, 'wb'))


# run the application!
if __name__ == '__main__':
     # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

