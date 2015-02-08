import requests
from random import randint

user = randint(1, 5)
print user
r = requests.post('http://178.62.45.23/post/%i' % user,
                  json={
                      'location': 0,
                      'accelerometer': 0,
                      'ringer': 1,
                      'call': 0,
                      'calendar': 0}
).text
print r