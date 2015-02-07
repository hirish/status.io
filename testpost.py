import requests
from random import randint

user = randint(1, 5)
print user
r = requests.post('http://localhost:5000/post/%i' % user,
                  json={
                      'location': 0,
                      'accelerometer': 1,
                      'ringer': 0,
                      'call': 1,
                      'calendar': 0}
).text
print r