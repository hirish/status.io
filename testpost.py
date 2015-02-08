import requests
from random import randint

user = randint(1, 5)
print user
r = requests.post('http://localhost:5000/post/%i' % user,
                  data={
                      'location': 0,
                      'accelerometer': 0,
                      'silent': 1,
                      'onCall': 0,
                      'calendar': 0,
                      'nextAlarm': "null",
                      'chrome': 1
                  }
).text
print r