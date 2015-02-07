import requests
from random import randint

print requests.post('http://localhost:5000/post/%i' % randint(1,5), json={'data': ['silent', 'true', 'onCall', 'false']}).text
